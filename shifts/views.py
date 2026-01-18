from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from wfm_core.shift import Shift

from .serializers import ShiftSerializer


class ShiftCreateView(APIView):
    def post(self, request):
        serializer = ShiftSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Pass data to domain model
            shift = Shift(
                staff_id=serializer.validated_data["staff_id"],
                date=serializer.validated_data["date"].isoformat(),  # ISO string YYYY-MM-DD
                start_time=serializer.validated_data["start_time"],  # time object
                end_time=serializer.validated_data["end_time"],
            )
        except (ValueError, TypeError) as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Return success response
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
