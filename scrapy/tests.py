import datetime
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from base.models import Person, Department, User
from .models import StationUserAndPassword
from rest_framework.reverse import reverse
from call_over.models import AttentionTable


# Create your tests here.

class TestScrapy(APITestCase):
    def setUp(self):
        department = Department.objects.create(
            name='test'
        )
        user = User.objects.create(username='test', password='111111')
        Person.objects.create(name='test', department=department, user=user)
        StationUserAndPassword.objects.create(
            username='章胜',
            password='123456',
            user=user
        )

    def test_get_url(self):
        self.client.force_login(User.objects.get(username='test'))
        department = Department.objects.first()
        table = AttentionTable.objects.create(
            department=department,
            date=datetime.datetime(2016,7,19),
            day_number=1
        )
        response = self.client.post(
            reverse('get-id'),
            data={'url': 'http://10.128.20.124/proBQYX/BQYXFX/BQPrint.aspx?ID=c823fb5f-07a7-4bec-a395-3b0eaf762e22',
                  'attend_table': table.pk}
        )
        self.assertEqual(response.status_code, 200, response.data)
