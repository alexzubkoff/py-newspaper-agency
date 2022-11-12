import unittest
from django.test import Client


class NewspaperTest(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_http_req_res_quantity_items_db(self):
        response = self.client.get("/redactors/search/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["redactor_list"]), 1)

        response = self.client.get("/redactors/search/?search=w")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["redactor_list"]), 0)

        response = self.client.get("/redactors/search/?search=adm")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["redactor_list"]), 0)

        response = self.client.get("/newspapers/search/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 6)

        response = self.client.get("/newspapers/search/?search=werw")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 0)

        response = self.client.get("/newspapers/search/?search=sun")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 2)

        response = self.client.get("/newspapers/search/?search=wall")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["newspaper_list"]), 2)

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

