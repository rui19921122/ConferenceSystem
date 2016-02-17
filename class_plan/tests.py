from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from . import models


# Create your tests here.


class TestClassPlan(APITestCase):
    def setUp(self):
        User.objects.create_superuser('hanrui', '1@qq.com', '111111')
        new = models.ClassPlanBase(name='111', number=2)
        new.save()

    def test_anonymous_put_request(self):
        self.client.logout()
        url = reverse('update_class_plan')
        res = self.client.put(url, {'name': '111'})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_post_request(self):
        self.client.logout()
        url = reverse('update_class_plan')
        res = self.client.post(url, {'name': '111'})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_none_update_class_plan(self):
        models.ClassPlanBase.objects.filter(number=1).delete()
        self.client.login(username='hanrui', password='111111')
        url = reverse('update_class_plan')
        res = self.client.put(url, {'name': '111', 'number': 1})
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_class_plan(self):
        self.client.login(username='hanrui', password='111111')
        url = reverse('update_class_plan')
        res = self.client.post(url, {'name': '111', 'number': 1})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.ClassPlanBase.objects.all().count(), 2)
        self.assertEqual(res.data, {'name': '111', 'number': 1})

    def test_conflict_post(self):
        self.client.login(username='hanrui', password='111111')
        url = reverse('update_class_plan')
        res = self.client.post(url, {'name': '111', 'number': 2})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_anoy_get_all(self):
        url = reverse('update_class_plan')
        res = self.client.get(path=url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_get_without_number(self):
        self.client.login(username='hanrui', password='111111')
        url = reverse('update_class_plan', )
        res = self.client.get(path=url)
        self.assertEqual(res.status_code, 400)

    def test_user_get_with_number(self):
        self.client.login(username='hanrui', password='111111')
        url = reverse('update_class_plan')
        res = self.client.get(path=url, data={'number': '2'})
        self.assertEqual(res.status_code, 400)

    def tearDown(self):
        User.objects.get(username='hanrui').delete()
