from rest_framework import generics
from .models import Data
from .serializers import DataSerializer

class DataListCreateView(generics.ListCreateAPIView):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
