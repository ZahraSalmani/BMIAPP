from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import SET_NULL


class BMI_History(models.Model):
    age = models.IntegerField()
    weight = models.FloatField()
    height = models.FloatField()
    name = models.CharField(max_length=25, null=True)
    created_at = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
