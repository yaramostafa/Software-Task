from django.shortcuts import render
from rest_framework import generics
from .models import KPI, AssetKPI
from .serializers import KPISerializer, AssetKPISerializer

# KPI Endpoints
class KPIListCreateView(generics.ListCreateAPIView):
    queryset = KPI.objects.all()
    serializer_class = KPISerializer

# Link Asset to KPI
class AssetKPICreateView(generics.CreateAPIView):
    queryset = AssetKPI.objects.all()
    serializer_class = AssetKPISerializer
