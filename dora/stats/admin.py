from django.contrib import admin

from dora.stats.models import (
    ABTestGroup,
    DeploymentState,
    DiMobilisationEvent,
    DiServiceView,
    MobilisationEvent,
    OrientationView,
    PageView,
    SearchView,
    ServiceView,
    StructureView,
)


class DeploymentStateAdmin(admin.ModelAdmin):
    list_display = ("department_code", "department_name", "state")
    list_filter = ["state"]
    list_editable = ["state"]
    list_per_page = 101
    ordering = ["department_code"]
    readonly_fields = ["department_code", "department_name"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


class AnalyticsEventAdmin(admin.ModelAdmin):
    date_hierarchy = "date"

    ordering = ("-id",)
    raw_id_fields = ["user"]


class PageViewAdmin(AnalyticsEventAdmin):
    list_display = [
        "date",
        "path",
        "user",
        "anonymous_user_hash",
        "title",
    ]
    list_filter = [
        "date",
        "is_staff",
        "is_logged",
    ]


@admin.display(description="Catégories")
def categories_display(obj):
    return ", ".join(c.label for c in obj.categories.all())


@admin.display(description="Sous-Catégories")
def subcategories_display(obj):
    return ", ".join(c.label for c in obj.subcategories.all())


class SearchEventAdmin(AnalyticsEventAdmin):
    list_display = [
        "date",
        "department",
        "city_code",
        categories_display,
        subcategories_display,
        "user",
        "anonymous_user_hash",
        "num_results",
    ]
    list_filter = [
        "date",
        "categories",
        "is_staff",
        "is_logged",
        "department",
    ]
    filter_horizontal = [
        "categories",
        "subcategories",
    ]


class StructureEventAdmin(AnalyticsEventAdmin):
    raw_id_fields = ("structure", "user")
    list_display = [
        "date",
        "path",
        "structure",
        "structure_department",
        "user",
        "anonymous_user_hash",
    ]
    list_filter = [
        "date",
        "structure_department",
        "structure_source",
    ]


class ServiceEventAdmin(AnalyticsEventAdmin):
    raw_id_fields = ("service", "structure", "user", "search_view")
    list_display = [
        "date",
        "service",
        "structure",
        "structure_department",
        "user",
        "anonymous_user_hash",
    ]
    list_filter = [
        "date",
        "structure_department",
        "structure_source",
        "service_source",
        "is_orientable",
        "status",
    ]
    filter_horizontal = [
        "categories",
        "subcategories",
    ]


class DiServiceEventAdmin(AnalyticsEventAdmin):
    raw_id_fields = ("user", "search_view")
    list_display = [
        "date",
        "service_name",
        "structure_name",
        "structure_department",
        "source",
        "user",
        "anonymous_user_hash",
    ]
    list_filter = ["date", "structure_department", "source"]
    filter_horizontal = [
        "categories",
        "subcategories",
    ]


class OrientationEventAdmin(AnalyticsEventAdmin):
    raw_id_fields = ("service", "structure", "user")
    list_display = [
        "date",
        "service",
        "structure",
        "structure_department",
        "user",
        "anonymous_user_hash",
    ]
    list_filter = [
        "date",
        "structure_department",
    ]
    filter_horizontal = [
        "categories",
        "subcategories",
    ]


@admin.display(description="AB groups")
def ab_testing_groups_display(obj):
    return ", ".join(c.value for c in obj.ab_test_groups.all())


class MobilisationEventAdmin(AnalyticsEventAdmin):
    raw_id_fields = ("service", "structure", "user", "search_view")
    list_display = [
        "date",
        ab_testing_groups_display,
        "service",
        "structure",
        "structure_department",
        "user",
        "anonymous_user_hash",
    ]

    list_filter = ["date", "structure_department", "ab_test_groups"]
    filter_horizontal = [
        "ab_test_groups",
        "categories",
        "subcategories",
    ]


class DiMobilisationEventAdmin(AnalyticsEventAdmin):
    raw_id_fields = ("user", "search_view")
    list_display = [
        "date",
        ab_testing_groups_display,
        "service_name",
        "structure_name",
        "structure_department",
        "user",
        "anonymous_user_hash",
    ]
    list_filter = ["date", "structure_department", "ab_test_groups"]
    filter_horizontal = ["categories", "subcategories", "ab_test_groups"]


admin.site.register(DeploymentState, DeploymentStateAdmin)
admin.site.register(PageView, PageViewAdmin)
admin.site.register(StructureView, StructureEventAdmin)
admin.site.register(OrientationView, OrientationEventAdmin)
admin.site.register(ServiceView, ServiceEventAdmin)
admin.site.register(DiServiceView, DiServiceEventAdmin)
admin.site.register(SearchView, SearchEventAdmin)
admin.site.register(MobilisationEvent, MobilisationEventAdmin)
admin.site.register(DiMobilisationEvent, DiMobilisationEventAdmin)

admin.site.register(ABTestGroup)
