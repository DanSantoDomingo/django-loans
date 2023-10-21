from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("loans-excel", views.LoanUploadView, "loan-uploads")
router.register("loans", views.LoanReadOnlyViewSet, "loans")
router.register(
    "amortization-schedules", views.AmortizationScheduleViewSet, "amortizations"
)

urlpatterns = [
    path("api/", include(router.urls)),
]
