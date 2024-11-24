from rest_framework import serializers
from .models import KPI, AssetKPI
import sqlite3

# Function to fetch distinct asset_ids from processed_data
def get_asset_ids():
    conn = sqlite3.connect('../processed_data.db') 
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT asset_id FROM processed_data")
    asset_ids = [row[0] for row in cursor.fetchall()]

    conn.close()

    return [(asset_id, asset_id) for asset_id in asset_ids]

class KPISerializer(serializers.ModelSerializer):
    class Meta:
        model = KPI
        fields = ['id', 'name', 'expression', 'description']


class AssetKPISerializer(serializers.ModelSerializer):
    asset_id = serializers.ChoiceField(choices=get_asset_ids()) 
    class Meta:
        model = AssetKPI
        fields = ['id', 'asset_id', 'kpi']
