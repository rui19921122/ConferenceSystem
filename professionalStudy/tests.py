from django.http import HttpRequest
from django.test import TestCase
from django.template.loader import render_to_string


# Create your tests here.
class TestView(TestCase):
    def test_home_page_returns_correct_html(self):
        request = HttpRequest()

