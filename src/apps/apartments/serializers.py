from rest_framework import serializers

from apartments.models import Apartment


class ApartmentSerializer(serializers.ModelSerializer):
    def get_distance(self, obj):
        if hasattr(obj, 'distance'):
            return round(obj.distance.km, 1)
        return None

    distance = serializers.SerializerMethodField(required=False)
    city = serializers.StringRelatedField()
    country = serializers.StringRelatedField()

    class Meta:
        model = Apartment
        fields = ('id', 'country', 'city',
                  'description', 'square_area',
                  'room_amount', 'bedroom_amount',
                  'daily_rate', 'convenience_items',
                  'average_rating', 'location', 'distance')
