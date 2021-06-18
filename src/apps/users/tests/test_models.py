from django.test import TestCase

from apartments.models import Country, City
from users.models import User

import tempfile


class UserModelTestCase(TestCase):
    def setUp(self):
        self.country = Country.objects.create(name='USA')
        self.city = City.objects.create(name='Washington', country=self.country)
        self.data = {
            'email': 'example@example.com',
            'password': 'example123',
            'confirm_password': 'example123',
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': 1,
            'birthday': '1979-1-1',
            'country': self.country.id,
            'city': self.city.id,
            'passport': tempfile.NamedTemporaryFile(suffix=".jpg").name,
        }

    def test_user_creation(self):
        User.objects.create(email=self.data['email'],
                            password=self.data['password'],
                            first_name=self.data['first_name'],
                            last_name=self.data['last_name'],
                            gender=self.data['gender'],
                            birthday=self.data['birthday'],
                            country_id=self.data['country'],
                            city_id=self.data['city'],
                            passport=self.data['passport'])
        self.assertTrue(User.objects.filter(email='example@example.com').exists())

    def test_str(self):
        user = User.objects.create(email=self.data['email'],
                                   password=self.data['password'],
                                   first_name=self.data['first_name'],
                                   last_name=self.data['last_name'],
                                   gender=self.data['gender'],
                                   birthday=self.data['birthday'],
                                   country_id=self.data['country'],
                                   city_id=self.data['city'],
                                   passport=self.data['passport'])
        self.assertEqual(user.email, str(user))
