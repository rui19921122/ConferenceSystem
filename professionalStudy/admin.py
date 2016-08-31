from django.contrib import admin
from .models import ProfessionalStudy

# Register your models here.
@admin.register(ProfessionalStudy)
class BaseAdmin(admin.ModelAdmin):
    pass
