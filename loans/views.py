from rest_framework.generics import CreateAPIView

from .serializers import LoanExcelSerializer


class LoanUploadView(CreateAPIView):
    serializer_class = LoanExcelSerializer
