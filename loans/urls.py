from django.urls import path

from .views import LoanUploadView

urlpatterns = [
    path("api/loans", LoanUploadView.as_view(), name="loans"),
]
