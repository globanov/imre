from rest_framework import serializers


class ShiftSerializer(serializers.Serializer):
    staff_id = serializers.IntegerField(min_value=1)
    date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
