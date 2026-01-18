from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class ShiftAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_shift(self):
        response = self.client.post(
            "/api/shifts/",
            {"staff_id": 17, "date": "2026-06-15", "start_time": "09:00", "end_time": "18:00"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        self.assertEqual(data["staff_id"], 17)
        self.assertEqual(data["date"], "2026-06-15")
        self.assertEqual(data["start_time"], "09:00:00")
        self.assertEqual(data["end_time"], "18:00:00")
        self.assertEqual(data["duration_hours"], 9.0)  # 9 часов

    def test_rejects_shift_shorter_than_1_hour(self):
        response = self.client.post(
            "/api/shifts/",
            {"staff_id": 17, "date": "2026-06-15", "start_time": "09:00", "end_time": "09:59"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("duration must be between 1 and 12 hours", str(response.data))
