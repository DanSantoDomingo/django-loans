from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import LoanReadOnlyViewSet, LoanUploadView

router = SimpleRouter()
router.register("loans", LoanReadOnlyViewSet)

urlpatterns = [
    path("api/loans/", LoanUploadView.as_view()),
    path("api/", include(router.urls)),
]
