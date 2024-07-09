from django.test import TestCase, SimpleTestCase
from http import HTTPStatus

# Create your tests here.
class KeepAliveTest(SimpleTestCase):
   def test_get(self):
       response = self.client.get('/keep-alive/')
       assert response.status_code == HTTPStatus.OK


class RobotsTxtTests(SimpleTestCase):
    def test_get(self):
        response = self.client.get("/robots.txt")

        assert response.status_code == HTTPStatus.OK
        assert response["content-type"] == "text/plain"