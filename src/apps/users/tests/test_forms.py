from django.core.exceptions import ValidationError
from django.test import Client, RequestFactory, TestCase
from django.shortcuts import reverse

from apartments.models import Country, City
from users.forms import RegisterForm

import tempfile


class RegisterFormTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        self.country = Country.objects.create(name='USA')
        self.city = City.objects.create(name='Washington', country=self.country)
        self.cleaned_data = {
            'email': 'example@example.com',
            'password': 'example123',
            'confirm_password': 'example123',
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': 1,
            'birthday': '1.1.1979',
            'country': self.country.id,
            'city': self.city.id,
            'passport': tempfile.NamedTemporaryFile(suffix=".jpg").name,
        }

    def test_register_form(self):
        form = RegisterForm(data=self.cleaned_data)
        self.assertTrue(form.is_valid())

    def test_register_form_wrong_data(self):
        wrong_data = {
            'email': 'bad_email',
            'password': 'S3CUR3@F',
            'confirm_password': 'bad_password',
            'first_name': 99,
            'last_name': 99,
            'gender': 4,
            'birthday': 'bad_date',
            'city': 'bad_city',
            'country': 'bad_country',
        }

        form = RegisterForm(data=wrong_data)
        self.assertFalse(form.is_valid())
        self.assertSetEqual(set(form.errors), set(wrong_data))

    def test_register_form_context(self):
        wrong_data = self.cleaned_data
        wrong_data['email'] = 'bad_email'
        response = self.c.post(reverse('register'), wrong_data)
        self.assertFormError(response, 'form', 'email', ['Enter a valid email address.'])
