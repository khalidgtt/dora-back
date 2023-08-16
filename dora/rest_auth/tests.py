from datetime import timedelta

from django.utils import timezone
from freezegun import freeze_time
from model_bakery import baker
from rest_framework.test import APITestCase

from dora.core.models import ModerationStatus
from dora.core.test_utils import make_structure
from dora.structures.models import Structure, StructureMember, StructurePutativeMember

DUMMY_SIRET = "12345678901234"


class CguTestCase(APITestCase):
    def test_no_cgu(self):
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)
        response = self.client.post("/auth/accept-cgu/")
        self.assertEqual(response.status_code, 400)

    def test_user_accepts_cgu(self):
        cgu_version = "20230714"
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)
        response = self.client.post("/auth/accept-cgu/", {"cgu_version": cgu_version})
        user.refresh_from_db()
        self.assertEqual(response.status_code, 204)
        self.assertIn(cgu_version, user.cgu_versions_accepted)

    def test_user_accepts_new_cgu_version(self):
        old_cgu_version = "20230715"
        cgu_version = "20230722"
        user = baker.make(
            "users.User",
            is_valid=True,
            cgu_versions_accepted={old_cgu_version: "2021-07-22T00:00:00+00:00"},
        )
        self.client.force_authenticate(user=user)
        response = self.client.post("/auth/accept-cgu/", {"cgu_version": cgu_version})
        user.refresh_from_db()
        self.assertEqual(response.status_code, 204)
        self.assertIn(old_cgu_version, user.cgu_versions_accepted)
        self.assertIn(cgu_version, user.cgu_versions_accepted)

    def test_no_overwrite_already_valided_cgu(self):
        cgu_version = "20230714"
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)

        response = self.client.post("/auth/accept-cgu/", {"cgu_version": cgu_version})
        user.refresh_from_db()
        self.assertEqual(response.status_code, 204)
        self.assertIn(cgu_version, user.cgu_versions_accepted)
        cgu_validation_datetime = user.cgu_versions_accepted[cgu_version]

        with freeze_time(timezone.now() + timedelta(days=2)):
            response = self.client.post(
                "/auth/accept-cgu/", {"cgu_version": cgu_version}
            )
            user.refresh_from_db()
            self.assertEqual(response.status_code, 204)
            self.assertIn(cgu_version, user.cgu_versions_accepted)
            self.assertEqual(
                cgu_validation_datetime, user.cgu_versions_accepted[cgu_version]
            )


class AuthenticationTestCase(APITestCase):
    def test_join_structure_creates_structure(self):
        baker.make("Establishment", siret=DUMMY_SIRET)
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)
        response = self.client.post(
            "/auth/join-structure/",
            {"siret": DUMMY_SIRET, "cguVersion": "20230805"},
        )
        self.assertEqual(response.status_code, 200)
        slug = response.data["slug"]
        structure = Structure.objects.get(slug=slug)
        self.assertEqual(structure.siret, DUMMY_SIRET)

    def test_cgu_required(self):
        baker.make("Establishment", siret=DUMMY_SIRET)
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)
        response = self.client.post(
            "/auth/join-structure/",
            {"siret": DUMMY_SIRET},
        )
        self.assertEqual(response.status_code, 400)

    def test_user_can_join_structure(self):
        baker.make("Establishment", siret=DUMMY_SIRET)
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)
        response = self.client.post(
            "/auth/join-structure/",
            {"siret": DUMMY_SIRET, "cguVersion": "20230805"},
        )
        self.assertEqual(response.status_code, 200)
        StructureMember.objects.get(structure__siret=DUMMY_SIRET, user=user)

    def test_first_user_in_structure_becomes_admin(self):
        baker.make("Establishment", siret=DUMMY_SIRET)
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)
        response = self.client.post(
            "/auth/join-structure/",
            {"siret": DUMMY_SIRET, "cguVersion": "20230805"},
        )
        self.assertEqual(response.status_code, 200)
        member = StructureMember.objects.get(structure__siret=DUMMY_SIRET, user=user)
        self.assertTrue(member.is_admin)

    def test_following_users_in_structure_becomes_putative(self):
        baker.make("Establishment", siret=DUMMY_SIRET)
        struct = make_structure(siret=DUMMY_SIRET)
        user = baker.make("users.User", is_valid=True)
        struct.members.add(
            user,
            through_defaults={
                "is_admin": True,
            },
        )
        user2 = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user2)
        response = self.client.post(
            "/auth/join-structure/",
            {"siret": DUMMY_SIRET, "cguVersion": "20230805"},
        )
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(StructureMember.DoesNotExist):
            StructureMember.objects.get(structure__siret=DUMMY_SIRET, user=user2)
        pm = StructurePutativeMember.objects.get(
            structure__siret=DUMMY_SIRET, user=user2
        )
        self.assertFalse(pm.is_admin)
        self.assertFalse(pm.invited_by_admin)

    def test_can_only_join_a_structure_once(self):
        baker.make("Establishment", siret=DUMMY_SIRET)
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)
        response = self.client.post(
            "/auth/join-structure/",
            {"siret": DUMMY_SIRET, "cguVersion": "20230805"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            StructureMember.objects.filter(
                structure__siret=DUMMY_SIRET, user=user
            ).count(),
            1,
        )
        response2 = self.client.post(
            "/auth/join-structure/",
            {"siret": DUMMY_SIRET, "cguVersion": "20230805"},
        )
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(
            StructureMember.objects.filter(
                structure__siret=DUMMY_SIRET, user=user
            ).count(),
            1,
        )

    def test_first_user_in_structure_changes_moderation_status(self):
        baker.make("Establishment", siret=DUMMY_SIRET)
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)
        response = self.client.post(
            "/auth/join-structure/",
            {"siret": DUMMY_SIRET, "cguVersion": "20230805"},
        )
        self.assertEqual(response.status_code, 200)

        structure = Structure.objects.get(siret=response.data["siret"])
        self.assertEqual(
            structure.moderation_status, ModerationStatus.NEED_INITIAL_MODERATION
        )

    def test_following_users_in_structure_dont_changes_moderation_status(self):
        baker.make("Establishment", siret=DUMMY_SIRET)
        struct = make_structure(
            siret=DUMMY_SIRET, moderation_status=ModerationStatus.VALIDATED
        )
        user = baker.make("users.User", is_valid=True)
        struct.members.add(
            user,
            through_defaults={
                "is_admin": True,
            },
        )
        user2 = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user2)
        response = self.client.post(
            "/auth/join-structure/",
            {"siret": DUMMY_SIRET, "cguVersion": "20230805"},
        )
        self.assertEqual(response.status_code, 200)
        structure = Structure.objects.get(siret=response.data["siret"])
        self.assertEqual(structure.moderation_status, ModerationStatus.VALIDATED)
