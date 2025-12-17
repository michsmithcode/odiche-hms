from rest_framework import serializers
from .models import Ward
from .models import Bed

class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = [
            "id",
            "name",
            "capacity",
            "location",
        ]



class BedSerializer(serializers.ModelSerializer):
    ward_name = serializers.CharField(source="ward.name", read_only=True)

    class Meta:
        model = Bed
        fields = [
            "id",
            "ward",
            "ward_name",
            "bed_number",
            "is_occupied",
        ]
