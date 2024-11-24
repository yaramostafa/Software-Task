from django.urls import path
from .views import KPIListCreateView, AssetKPICreateView

urlpatterns = [
    path('kpis/', KPIListCreateView.as_view(), name='kpi-list-create'),
    path('assets/link/', AssetKPICreateView.as_view(), name='asset-kpi-link'),
    path('', KPIListCreateView.as_view(), name='kpi-list-create'),
]
