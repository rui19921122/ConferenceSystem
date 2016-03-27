
from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Department,models.Person)
class ModelAdmin(admin.ModelAdmin):
    pass
