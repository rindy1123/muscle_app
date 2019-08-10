from django.contrib import admin
from .models import WorkoutModel, DietModel, BodyModel
# Register your models here.

admin.site.register(WorkoutModel)
admin.site.register(DietModel)
admin.site.register(BodyModel)
