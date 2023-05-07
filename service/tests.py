from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import ServiceUser


class ServiceUserTests(APITestCase):
    def test_restaurant_detail(self):
        response = self.client.get('/restaurant/')
        self.assertEqual(response.data, {'id': 1, 'name': 'Пузата Хата'})

    def test_create_user(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('/service_user/')
        data = {'username': 'user'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ServiceUser.objects.count(), 1)
        self.assertEqual(ServiceUser.objects.get().first_name, 'Name')
