from django.test import TestCase
from rest_framework.test import APIClient

from wfm_core.worker import workload_store


class EndToEndTest(TestCase):
    def tearDown(self):
        workload_store.clear()

    def test_create_shift_updates_weekly_workload(self):
        client = APIClient()
        response = client.post(
            "/api/shifts/",
            {"staff_id": 17, "date": "2026-06-15", "start_time": "09:00", "end_time": "18:00"},
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        # Verify WeeklyWorkload was updated
        key = (17, "2026-06-15")
        self.assertIn(key, workload_store)
        self.assertEqual(workload_store[key].total_hours, 9.0)
