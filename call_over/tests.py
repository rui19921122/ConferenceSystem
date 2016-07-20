from django.test import TestCase
from rest_framework.test import APITestCase

# Create your tests here.
class Test(APITestCase):
    def __init__(self):
        super(Test, self).__init__()

    def setUp(self):
        pass
