from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Loan
from .serializers import LoanExcelSerializer, LoanSerializer


class LoanUploadView(CreateAPIView):
    serializer_class = LoanExcelSerializer


class LoanReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
