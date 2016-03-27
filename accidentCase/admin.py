from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Accident)
class ModelAdmin(admin.ModelAdmin):
    pass
