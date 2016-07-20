from django.contrib import admin
from .models import ScrapyData,StationUserAndPassword

# Register your models here.
@admin.register(ScrapyData,StationUserAndPassword)
class DefaultAdmin(admin.ModelAdmin):
    pass

