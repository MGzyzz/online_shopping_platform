from django.test import TestCase
from django.urls import reverse

from .models import User


class LoginTestCase(TestCase):
    def setUp(self):
        self.username = 'username@gmail.com'
        self.password = '123123'
        self.user = User.objects.create_user(email=self.username, password=self.password, phone='77054779047')

        self.login_url = reverse('login')

    def test_user_login(self):
        data = {'username': self.username, 'password': self.password}

        response = self.client.post(self.login_url, data)

        self.assertRedirects(response, reverse('home'))

    def test_user_login_fail(self):
        data = {'username': self.username, 'password': 'wrongpass'}

        response = self.client.post(self.login_url, data)

        self.assertContains(response, 'Please enter a correct Email and password. Note that both fields may be case-sensitive.')


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.registration_url = 'register'

    def test_registration_success(self):
        data = {'first_name': 'John', 'last_name': 'Doe', 'phone': '77054779047', 'email': 'johndoe@gmail.com', 'password1': '123', 'password2': '123'}




