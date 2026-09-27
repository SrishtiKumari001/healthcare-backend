from rest_framework.routers import DefaultRouter
from .views import PatientDoctorMappingViewSet

router = DefaultRouter(trailing_slash=True)
router.register(r"", PatientDoctorMappingViewSet, basename="mapping")

urlpatterns = router.urls
