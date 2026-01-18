from django.test import TestCase
from rest_framework.test import APIClient

from wfm_core.worker import workload_store


class WorkloadAPITest(TestCase):
    def tearDown(self):
        workload_store.clear()

    def test_get_workload_for_existing_staff_and_week(self):
        # Предварительно создадим данные через API
        client = APIClient()
        client.post(
            "/api/shifts/",
            {"staff_id": 17, "date": "2026-06-15", "start_time": "09:00", "end_time": "18:00"},
            format="json",
        )

        # Запрос агрегата
        response = client.get("/api/workload/staff/17/week/2026-06-15/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["staff_id"], 17)
        self.assertEqual(data["week_start"], "2026-06-15")
        self.assertEqual(data["total_hours"], 9.0)

    def test_get_workload_returns_404_if_not_found(self):
        client = APIClient()
        response = client.get("/api/workload/staff/999/week/2026-06-15/")
        self.assertEqual(response.status_code, 404)
