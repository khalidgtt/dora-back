"""dora URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path, register_converter
from rest_framework.routers import SimpleRouter

import dora.core.views
import dora.rest_auth
import dora.services.views
import dora.sirene.views
import dora.structures.views

from .url_converters import InseeCodeConverter, SiretConverter

router = SimpleRouter()
router.register(
    r"structures", dora.structures.views.StructureViewSet, basename="structure"
)
router.register(
    r"structure-members",
    dora.structures.views.StructureMemberViewset,
    basename="structure-member",
)
router.register(
    r"structure-putative-members",
    dora.structures.views.StructurePutativeMemberViewset,
    basename="structure-putative-member",
)
router.register(r"services", dora.services.views.ServiceViewSet, basename="service")

register_converter(InseeCodeConverter, "insee_code")
register_converter(SiretConverter, "siret")


urlpatterns = [
    path("auth/", include("dora.rest_auth.urls")),
    path("search/", dora.services.views.search),
    path("search-sirene/<insee_code:citycode>/", dora.sirene.views.search_sirene),
    path("search-safir/", dora.structures.views.search_safir),
    path("search-siret/", dora.sirene.views.search_siret),
    path("search-all-sirene/", dora.sirene.views.search_all_sirene),
    path("services-options/", dora.services.views.options),
    path("siret-claimed/<siret:siret>/", dora.structures.views.siret_was_claimed),
    path("structures-options/", dora.structures.views.options),
    path("upload/<slug:structure_slug>/<str:filename>/", dora.core.views.upload),
    path("admin/", admin.site.urls),
    path("ping/", dora.core.views.ping),
    path("sentry-debug/", dora.core.views.trigger_error),
    path("", include(router.urls)),
]
