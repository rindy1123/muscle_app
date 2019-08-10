from django.db import models
from django.utils.timezone import localdate
# Create your models here.


# 筋トレメニューのモデル
class WorkoutModel(models.Model):
    name = models.CharField(max_length=100)
    weight = models.FloatField()
    reps = models.IntegerField()
    set = models.IntegerField()
    date = models.DateField(default=localdate())
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 食事データのモデル
class DietModel(models.Model):
    calorie = models.FloatField()
    name = models.CharField(max_length=100)
    protein = models.FloatField()
    carb = models.FloatField()
    fat = models.FloatField()
    date = models.DateField(default=localdate())
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# 身体データのモデル
class BodyModel(models.Model):
    weight = models.FloatField()
    percent_body_fat = models.FloatField(default=0)
    muscle_mass = models.FloatField(default=0)
    date = models.DateField(default=localdate())
    maintenance_calorie = models.FloatField(default=0)
    cutting_calorie = models.FloatField(default=0)
    increasing_calorie = models.FloatField(default=0)
    author = models.CharField(max_length=100)

