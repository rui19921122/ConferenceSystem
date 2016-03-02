from django.test import TestCase
from rest_framework.test import APITestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Create your tests here.
class Test(APITestCase):
    def setUp(self):
        new = User.objects.create_user(username='hanrui', password='111111')
        new.save()

    def test_login(self):
        url = reverse('rest_login')
        data = {'username': 'hanrui', 'password': '111111'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()

    def test_get_menu(self):
        url = reverse('getMenu')
        self.client.login(username='hanrui', password='111111')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        a = User.objects.get(username='hanrui')
        a.delete()
