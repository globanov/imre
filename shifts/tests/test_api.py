from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from wfm_core.events import ShiftCreated


class ShiftAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_shift(self):
        with patch("shifts.views.publish") as mock_publish:
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
            self.assertEqual(data["duration_hours"], 9.0)  # 9 hours

            # Verify event was published
            mock_publish.assert_called_once()
            args, _ = mock_publish.call_args
            event = args[0]
            assert isinstance(event, ShiftCreated)
            assert event.staff_id == 17
            assert event.duration_hours == 9.0

    def test_rejects_shift_shorter_than_1_hour(self):
        with patch("shifts.views.publish") as mock_publish:
            response = self.client.post(
                "/api/shifts/",
                {"staff_id": 17, "date": "2026-06-15", "start_time": "09:00", "end_time": "09:59"},
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            # noinspection PyUnresolvedReferences
            self.assertIn("duration must be between 1 and 12 hours", str(response.data))
            mock_publish.assert_not_called()

    def test_rejects_non_integer_staff_id(self):
        with patch("shifts.views.publish") as mock_publish:
            response = self.client.post(
                "/api/shifts/",
                {
                    "staff_id": "not-a-number",
                    "date": "2026-06-15",
                    "start_time": "09:00",
                    "end_time": "18:00",
                },
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            # noinspection PyUnresolvedReferences
            self.assertIn("staff_id", response.data)
            mock_publish.assert_not_called()

    def test_rejects_start_time_not_before_end_time(self):
        with patch("shifts.views.publish") as mock_publish:
            response = self.client.post(
                "/api/shifts/",
                {"staff_id": 17, "date": "2026-06-15", "start_time": "18:00", "end_time": "09:00"},
                format="json",
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            # noinspection PyUnresolvedReferences
            self.assertIn("start_time must be before end_time", str(response.data))
            mock_publish.assert_not_called()
