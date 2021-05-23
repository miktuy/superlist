from django.http import HttpResponse
from django.test import TestCase


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response: HttpResponse = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')