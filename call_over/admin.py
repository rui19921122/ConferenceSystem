from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.CallOverDetail, models.CallOverNumber)
class ModelAdmin(admin.ModelAdmin):
    pass
