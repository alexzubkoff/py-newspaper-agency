import unittest
from django.test import Client
from django.urls import reverse

from newspaper.models import Redactor


class NewspaperTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_http_req_res_quantity_items_db(self):
        response = self.client.get("/redactors/search/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["redactor_list"]), 3)

        response = self.client.get("/redactors/search/?search=w")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["redactor_list"]), 0)

        response = self.client.get("/redactors/search/?search=adm")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["redactor_list"]), 0)

        response = self.client.get("/newspapers/search/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 7)

        response = self.client.get("/newspapers/search/?search=werw")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 0)

        response = self.client.get("/newspapers/search/?search=sun")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 1)

        response = self.client.get("/newspapers/search/?search=wall")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 1)

        response = self.client.get("/topics/search/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["topic_list"]), 6)

        response = self.client.get("/topics/search/?search=weather")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["topic_list"]), 1)

        response = self.client.get("/topics/search/?search=politics")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["topic_list"]), 1)

        response = self.client.get("/topics/search/?search=re")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["topic_list"]), 0)

        response = self.client.get("/topics/search/?search=sport")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["topic_list"]), 0)

    def test_login(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {
            'username': 'testuser',
            'email': 'foo@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'latitude': '45',
            'longitude': '2',
            'country': 'FR',
            'location_description': 'Somewhere',
            'privacy_search': 'public',
            'privacy_email': 'private',
            'privacy_im': 'private',
            'privacy_irctrack': 'public',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Redactor.objects.count(), 3)

        data['password1'] = 'secret'
        data['password2'] = 'othersecret'
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Redactor.objects.count(), 3)
