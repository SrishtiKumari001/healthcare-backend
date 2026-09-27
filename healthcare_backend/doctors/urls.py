from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet

router = DefaultRouter(trailing_slash=True)
router.register(r"", DoctorViewSet, basename="doctor")

urlpatterns = router.urls
