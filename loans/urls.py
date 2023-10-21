from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("loans", views.LoanReadOnlyViewSet)
router.register("amortization-schedules", views.AmortizationScheduleViewSet)

urlpatterns = [
    path("api/loans/", views.LoanUploadView.as_view()),
    path("api/", include(router.urls)),
]
