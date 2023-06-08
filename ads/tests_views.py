from django.test import TestCase, Client
from .models import WebsiteUser
from django.contrib.messages import get_messages


class MyTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_index_page(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=/')

    def test_error_page(self):
        response = self.client.get('error')
        self.assertEqual(response.status_code, 404)

    def test_delete_user(self):
        user = WebsiteUser.objects.create_user(username='test', password='password')
        self.client.force_login(user)
        response = self.client.get('/users/delete/1')
        print(get_messages(response))
        print(response)
