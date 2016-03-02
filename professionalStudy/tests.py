from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from base.models import Department, ProfessionalSystem, Person
from professionalStudy.models import ProfessionalStudy


# Create your tests here.
class TestProfessionalStudy(APITestCase):
    '''
    测试业务学习相关API
    '''

    def setUp(self):
        test_system = ProfessionalSystem.objects.create(name='测试专业系统')
        test_department = Department.objects.create(name='测试部门',
                                                    system=test_system)
        test_user = User.objects.create_user(username='test', password='111111')
        Person.objects.create(name='测试用户',
                              department=test_department,
                              user=test_user)
        self.client.force_login(test_user)

    def test_post_professional_study(self):
        data = {'content': ''.join('测试数据重复100次' for a in range(100))}
        url = reverse('professionalStudy')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProfessionalStudy.objects.count(), 1)
        self.assertEqual(ProfessionalStudy.objects.first().content,
                         data.get('content'))

    def test_get_undone_professional_study(self):
        data1 = {'content': ''.join('测试数据重复100次' for a in range(100))}
        data2 = {'content': ''.join('测试数据' for a in range(100))}
        url = reverse('professionalStudy')
        self.client.post(url, data=data1)
        self.client.post(url, data=data2)
        url = reverse('professionalStudy')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2, response.data)
        self.assertIn(response.data[0].get('content'),
                      (data1.get('content'), data2.get('content')))

    def test_post_study(self):
        data1 = {'content': ''.join('测试数据重复100次' for a in range(100))}
        data2 = {'content': ''.join('测试数据' for a in range(100))}
        url = reverse('professionalStudy')
        self.client.post(url, data=data1)
        self.client.post(url, data=data2)
        url = reverse('professionalStudyPostStudy')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, response.data)
