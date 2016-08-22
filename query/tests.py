from django.test import TestCase
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from base.models import Person, Department, User


# Create your tests here.

class TestQueryList(APITestCase):
    def setUp(self):
        f = Department(is_superuser=False, name='调度车间')
        f.save()
        Department.objects.create(is_superuser=False, name='出发场车间')
        b = Department(is_superuser=True, name='站领导')
        b.save()
        self.custom_user = Person(name='test', department=f, user=User.objects.create(username='test',
                                                                                      password='111111'))
        self.custom_user.save()
        self.super_user = Person(name='super', department=b, user=User.objects.create(username='super',
                                                                                      password='111111'))
        self.super_user.save()

    def test_custom_person_get_data(self):
        '''
        测试普通用户的请求，有时间段
        :return:
        '''
        url = reverse('query-call-over')
        self.client.force_login(User.objects.get(username='test'))
        response = self.client.get(url, data={'start': '2016-7-20', 'end': '2016-8-31'})
        assert isinstance(response, Response)
        assert self.assertEqual(response.status_code, 201, response.data)

    def test_custom_person_get_data_without_time(self):
        '''
        测试普通用户的请求，无时间段
        :return:
        '''
        url = reverse('query-call-over')
        self.client.force_login(User.objects.get(username='test'))
        response = self.client.get(url)

