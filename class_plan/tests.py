from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from base.models import Person, Department
from class_plan.models import ClassPlanBase, WhichDepartmentCanEditClassPlan
from rest_framework.parsers import JSONParser
from base.models import ProfessionalSystem

from . import models


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
        url = reverse('update_class_plan')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        self.assertEqual(len(response.data), 2, response.data)
        self.client.logout()

    def test_post_class_plan_base_by_other(self):
        self.client.login(username='not_allowed', password='111111')
        url = reverse('update_class_plan')
        response = self.client.post(url, data={'name': 'test3', 'number': '3'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)

    def test_post_class_plan_base_by_allowed_person(self):
        self.client.login(username='allowed', password='111111')
        url = reverse('update_class_plan')
        response = self.client.post(url, data={'name': 'test3', 'number': '3'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(len(response.data), 3, response.data)

    def test_get_class_plan_base(self):
        self.client.login(username='allowed', password='111111')
        url = reverse('get_class_plan', 1)
        response = self.client.post(url, data={'name': 'test3', 'number': '3'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertEqual(len(response.data), 3, response.data)
