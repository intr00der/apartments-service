from django.test import Client, RequestFactory, TestCase
from django import forms

from apartments.models import Country, City
from django.urls import reverse
from users.forms import RegisterForm
from users.managers import UserManager
from users.models import User
from users.views import register, auth_login

import tempfile
import json


class UserManagerTestCase(TestCase, UserManager):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.country = Country.objects.create(name='USA')
        self.city = City.objects.create(name='Washington', country=self.country)
        self.login_user = User.objects.create(
            email='example@EXAMPLE.com',
            password='example123',
            first_name='John',
            last_name='Doe',
            gender=1,
            birthday='1979-1-1',
            country_id=self.country.id,
            city_id=self.city.id,
            passport=tempfile.NamedTemporaryFile(suffix=".jpg").name
        )
        self.data = {'email': 'example@example.com',
                     'password': 'example123',
                     'confirm_password': 'example123',
                     'first_name': 'John',
                     'last_name': 'Doe',
                     'gender': 1,
                     'birthday': '1979-1-1',
                     'country': self.country.id,
                     'city': self.city.id}

    def test_register(self):
        request = self.factory.post('register/', self.data)
        response = register(request)
        self.assertEqual(response.status_code, 200)

    def test_register_put_request(self):
        new_data = self.data
        new_data['email'] = 'testing@example.com'
        request = self.factory.put('register/', self.data)
        register(request)
        self.assertEqual(
            User.objects.filter(email=new_data['email']).exists(), False)

    def test_login(self):
        data = {
            'email': self.login_user.email,
            'password': self.login_user.password
        }
        request = self.factory.post('login/', data)
        response = auth_login(request)
        self.assertEqual(response.status_code, 200)
