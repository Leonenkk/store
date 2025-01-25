
from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class RegistrationTestCase(TestCase):
    def setUp(self):
        self.path = reverse('users:registration')
        self.data = {
            'first_name': ' Maksimka',
            'last_name': 'Lennko',
            'email': 'oracle45@gmail.com',
            'password1': '16YjZ2005',
            'password2': '16YjZ2005',
            'username': 'VanyaR',
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')

    def test_user_registration_post_success(self):
        self.assertFalse(User.objects.filter(username=self.data['username']).exists())
        response = self.client.post(self.path, self.data)
        username=self.data['username']
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(User.objects.filter(username=username).exists())

        email_verification=EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now()+timedelta(hours=24)).date()
        )

    def test_user_registration_post_error(self):
        username=self.data['username']
        user=User.objects.create(username=username)
        response = self.client.post(self.path, self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.',html=True)




