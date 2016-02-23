from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from base.models import Person, Department
from base.models import ProfessionalSystem
from class_plan.models import WhichDepartmentCanEditClassPlan
from . import models
from .data_for_test import publish_class_plan_data


# Create your tests here.


class TestApiBase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super(TestApiBase, cls).setUpClass()
        cls.new = models.ClassPlanBase(name='test1', number='1')
        cls.new.save()
        cls.new1 = models.ClassPlanBase(name='test2', number='2')
        cls.new1.save()

    def setUp(self):
        system = ProfessionalSystem(name='接发列车')
        system.save()
        new_department = Department(name='调度车间', system=system)
        new_department.save()
        not_allowed_department = Department(name='出发', system=system)
        not_allowed_department.save()
        WhichDepartmentCanEditClassPlan(department=new_department).save()
        user = User.objects.create_user(username='allowed', password='111111')
        f = Person(name='test', department=new_department, user=user)
        f.save()
        user = User.objects.create_user(username='not_allowed', password='111111')
        f = Person(name='test', department=not_allowed_department, user=user)
        f.save()

    def test_list_class_plan_base(self):
        self.client.login(username='hanrui', password='111111')
        url = reverse('class-plan-base-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 2, response.data)
        self.client.logout()

    def test_post_class_plan_base_by_other(self):
        self.client.login(username='not_allowed', password='111111')
        url = reverse('class-plan-base-list')
        response = self.client.post(url, data={'name': 'test3', 'number': '3'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)

    def test_post_class_plan_base_by_allowed_person(self):
        self.client.login(username='allowed', password='111111')
        url = reverse('class-plan-base-list')
        response = self.client.post(url, data={'name': 'test3', 'number': '3'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(len(response.data), 3, response.data)

    def test_get_class_plan_base(self):
        '''
        测试获取指定班计划
        :return:
        '''
        self.client.login(username='allowed', password='111111')
        url = reverse('class-plan-base-detail', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

    def test_update_class_plan_base(self):
        self.client.login(username='allowed', password='111111')
        url = reverse('class-plan-base-detail', args=[1])
        data = {'number': 1, 'name': 'test5', url: url}
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.status_code)


class TestPostClassPlan(APITestCase):
    def setUp(self):
        system = ProfessionalSystem(name='接发列车')
        system.save()
        new_department = Department(name='调度车间', system=system)
        new_department.save()
        not_allowed_department = Department(name='出发', system=system)
        not_allowed_department.save()
        WhichDepartmentCanEditClassPlan(department=new_department).save()
        user = User.objects.create_user(username='allowed', password='111111')
        f = Person(name='test', department=new_department, user=user)
        f.save()
        user = User.objects.create_user(username='not_allowed', password='111111')
        f = Person(name='test', department=not_allowed_department, user=user)
        f.save()

    def test_post_data(self):
        self.client.login(username='allowed', password='111111')
        url = reverse('class-plan')
        response = self.client.post(url, data=publish_class_plan_data)
        self.assertEqual(response.data, status.HTTP_201_CREATED, response.data)
