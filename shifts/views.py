from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from wfm_core.events import ShiftCreated
from wfm_core.shift import Shift

from .event_publisher import publish
from .models import WeeklyWorkload
from .serializers import ShiftSerializer


class ShiftCreateView(APIView):
    def post(self, request):
        serializer = ShiftSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            shift = Shift(
                staff_id=serializer.validated_data["staff_id"],
                date=serializer.validated_data["date"].isoformat(),
                start_time=serializer.validated_data["start_time"],
                end_time=serializer.validated_data["end_time"],
            )
        except (ValueError, TypeError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        event = ShiftCreated(
            staff_id=shift.staff_id,
            date=shift.date,
            start_time=shift.start_time.isoformat(),
            end_time=shift.end_time.isoformat(),
            duration_hours=shift.duration_hours,
        )
        publish(event)

        return Response(
            {
                "staff_id": shift.staff_id,
                "date": shift.date,
                "start_time": shift.start_time.isoformat(),
                "end_time": shift.end_time.isoformat(),
                "duration_hours": shift.duration_hours,
            },
            status=status.HTTP_201_CREATED,
        )


class WorkloadRetrieveView(APIView):
    def get(self, request, staff_id: int, week_start: str):
        try:
            workload = WeeklyWorkload.objects.get(staff_id=staff_id, week_start=week_start)
        except WeeklyWorkload.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "staff_id": workload.staff_id,
                "week_start": workload.week_start.isoformat(),
                "total_hours": workload.total_hours,
            }
        )
