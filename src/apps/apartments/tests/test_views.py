from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from django.contrib.gis.geos import Point

from apartments.models import Apartment, Country, City
from apartments.views import HomeViewSet
from users.models import User

import tempfile


class HomeViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.country = Country.objects.create(name='USA')
        self.city = City.objects.create(name='Washington', country=self.country)
        self.owner = User.objects.create(email='example@example.com',
                                         password='asdfwew121',
                                         first_name='John',
                                         last_name='Doe',
                                         gender=1,
                                         birthday='1979-1-1',
                                         country_id=self.country.id,
                                         city_id=self.city.id,
                                         passport=tempfile.NamedTemporaryFile(suffix=".jpg").name)

        Apartment.objects.create(
            owner=self.owner,
            country=self.country,
            city=self.city,
            description='Nice apartment',
            square_area=25,
            room_amount=2,
            bedroom_amount=2,
            daily_rate=80,
            registry_ordering=tempfile.NamedTemporaryFile(suffix=".jpg").name,
            convenience_items=['COND', 'HRDR'],
            opens_at='2021-6-18',
            closes_at='2021-6-30',
            location=Point(x=30, y=50, srid=4326),
            is_verified=True
        )

    def test_filter_by_fitting_params(self):
        data = {
            'search_bar': 'Nice',
            'square_area': 20,
            'room_amount': 2,
            'bedroom_amount': 1,
            'daily_rate': 90,
            'convenience_items[]': 'COND',
        }
        response = self.client.get('/api/v1/home/', data=data)
        self.assertEqual(response.data['count'], 1)

    def test_get_apartment_list(self):
        response = self.client.get('/api/v1/home/')
        self.assertEqual(response.data['count'], 1)

    def test_filter_by_search_bar(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/home/', data={'search_bar': 'bad'})
        self.assertEqual(response.data['count'], 0)

    def test_filter_by_square_area(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/home/', data={'square_area': 99})
        self.assertEqual(response.data['count'], 0)

    def test_filter_by_daily_rate(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/home/', data={'daily_rate': 10})
        self.assertEqual(response.data['count'], 0)

    def test_filter_by_room_amount(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/home/', data={'room_amount': 3})
        self.assertEqual(response.data['count'], 0)

    def test_filter_by_bedroom_amount(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/home/', data={'bedroom_amount': 3})
        self.assertEqual(response.data['count'], 0)

    def test_filter_by_convenience_items(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/home/', data={'convenience_items[]': 'CLLN'})
        self.assertEqual(response.data['count'], 0)

    def test_order_by_location_with_added_distance(self):
        response = self.client.get('http://127.0.0.1:8000/api/v1/home/', data={'location': '50,30'})
        self.assertEqual(response.data['results'][0]['distance'], 0)
