from django.core.files.storage import default_storage
from rest_framework import serializers

from dora.structures.models import Structure

from .models import (
    BeneficiaryAccessMode,
    CoachOrientationMode,
    LocationKind,
    Service,
    ServiceCategories,
    ServiceKind,
    ServiceSubCategories,
)


class ServiceSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()
    forms_info = serializers.SerializerMethodField()
    structure = serializers.SlugRelatedField(
        queryset=Structure.objects.all(), slug_field="slug"
    )
    kinds_display = serializers.SerializerMethodField()
    categories_display = serializers.SerializerMethodField()
    subcategories_display = serializers.SerializerMethodField()
    access_conditions_display = serializers.SerializerMethodField()
    concerned_public_display = serializers.SerializerMethodField()
    requirements_display = serializers.SerializerMethodField()
    credentials_display = serializers.SerializerMethodField()
    location_kinds_display = serializers.SerializerMethodField()
    beneficiaries_access_modes_display = serializers.SerializerMethodField()
    coach_orientation_modes_display = serializers.SerializerMethodField()
    recurrence_display = serializers.CharField(
        source="get_recurrence_display", read_only=True
    )

    class Meta:
        model = Service
        # Temporary, while working on the exact model content
        exclude = ["id"]
        lookup_field = "slug"

    def get_is_available(self, obj):
        return True

    def get_forms_info(self, obj):
        forms = [{"name": form, "url": default_storage.url(form)} for form in obj.forms]
        return forms

    def get_kinds_display(self, obj):
        return [ServiceKind(kind).label for kind in obj.kinds]

    def get_location_kinds_display(self, obj):
        return [LocationKind(kind).label for kind in obj.location_kinds]

    def get_categories_display(self, obj):
        return [ServiceCategories(cat).label for cat in obj.categories]

    def get_subcategories_display(self, obj):
        return [ServiceSubCategories(cat).label for cat in obj.subcategories]

    def get_beneficiaries_access_modes_display(self, obj):
        return [
            BeneficiaryAccessMode(mode).label for mode in obj.beneficiaries_access_modes
        ]

    def get_coach_orientation_modes_display(self, obj):
        return [
            CoachOrientationMode(mode).label for mode in obj.coach_orientation_modes
        ]

    def get_access_conditions_display(self, obj):
        return [item.name for item in obj.access_conditions.all()]

    def get_concerned_public_display(self, obj):
        return [item.name for item in obj.concerned_public.all()]

    def get_requirements_display(self, obj):
        return [item.name for item in obj.requirements.all()]

    def get_credentials_display(self, obj):
        return [item.name for item in obj.credentials.all()]
