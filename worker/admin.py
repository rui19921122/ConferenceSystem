from django.contrib import admin
from .models import Position, Worker


# Register your models here.
@admin.register(Position, Worker)
class ModelAdmin(admin.ModelAdmin):
    pass
