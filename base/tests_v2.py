from rest_framework import test
from rest_framework.reverse import reverse


class TestMenu(test.APITestCase):
    def setUp(self):
        pass

    def test_get_menu(self):
        url = reverse('get-menu')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

