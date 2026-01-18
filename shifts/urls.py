from django.urls import path

from .views import ShiftCreateView, WorkloadRetrieveView

urlpatterns = [
    path("shifts/", ShiftCreateView.as_view(), name="shift-create"),
    path(
        "workload/staff/<int:staff_id>/week/<str:week_start>/",
        WorkloadRetrieveView.as_view(),
        name="workload-retrieve",
    ),
]
