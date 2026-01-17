from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class ShiftAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_shift(self):
        response = self.client.post('/api/shifts/', {
            "staff_id": 17,
            "date": "2026-06-15",
            "start_time": "09:00",
            "end_time": "18:00"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
