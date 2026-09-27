from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Healthcare Backend API",
        default_version="v1",
        description="Secure Django REST Framework backend for managing patients, "
                     "doctors and patient-doctor mappings, with JWT authentication.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # Dashboard UI (served by Django itself)
    path("", TemplateView.as_view(template_name="index.html"), name="dashboard"),

    # API
    path("api/auth/", include("accounts.urls")),
    path("api/patients/", include("patients.urls")),
    path("api/doctors/", include("doctors.urls")),
    path("api/mappings/", include("mappings.urls")),

    # Docs
    path("api/docs/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-docs"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
