from django.test import TestCase

from apartments.models import Country, City
from users.managers import UserManager
from users.models import User

import tempfile


class UserManagerTestCase(TestCase, UserManager):
    def setUp(self):
        self.country = Country.objects.create(name='USA')
        self.city = City.objects.create(name='Washington', country=self.country)

    def test_create_user(self):
        UserManager.create_user(
            self=User.objects,
            email='example@EXAMPLE.com',
            password='example123',
            first_name='John',
            last_name='Doe',
            gender=1,
            birthday='1979-1-1',
            country=self.country,
            city=self.city,
            passport=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )
        self.assertTrue(User.objects.filter(email='example@example.com').exists())

    def test_create_superuser(self):
        UserManager.create_superuser(
            self=User.objects,
            email='example_admin@EXAMPLE.com',
            password='example123',
            first_name='John',
            last_name='Doe',
            gender=1,
            birthday='1979-1-1',
            country=self.country,
            city=self.city
        )
        self.assertTrue(User.objects.filter(email='example_admin@example.com').exists())
