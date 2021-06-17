from rest_framework import serializers

from apartments.models import Apartment


class ApartmentSerializer(serializers.ModelSerializer):
    def get_distance(self, obj):
        if hasattr(obj, 'distance'):
            return round(obj.distance.km, 1)
        return None

    distance = serializers.SerializerMethodField(required=False)

    class Meta:
        model = Apartment
        fields = '__all__'
