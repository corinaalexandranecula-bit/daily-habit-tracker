from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    target_daily = models.IntegerField(default=1)
    color= models.CharField(max_length=7, default="#3498db")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#class HabitProgress(models.Model):
   # habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    #date = models.DateField()
    #completed = models.BooleanField(default=False)

    #def __str__(self):
      #  status = "Done" if self.completed else "Pending"
       # return f"{self.habit.title} - {self.date} - {status}"
    
class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="logs")
    date = models.DateField(default=timezone.localdate)
    done = models.BooleanField(default=True)

    class Meta:
        unique_together = ("habit", "date")
