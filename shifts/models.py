from django.db import models


class WeeklyWorkload(models.Model):
    staff_id = models.PositiveIntegerField()
    week_start = models.DateField()  # ISO Monday
    total_hours = models.FloatField(default=0.0)

    class Meta:
        unique_together = ("staff_id", "week_start")
        db_table = "weekly_workload"

    def __str__(self):
        return f"Staff {self.staff_id}, Week {self.week_start}: {self.total_hours}h"
