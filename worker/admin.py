from django.contrib import admin
from .models import Position, Worker, Figure, FigureSetting,AttentionTable,AttentionDetail


# Register your models here.
@admin.register(Position, Worker, Figure, FigureSetting,AttentionTable,AttentionDetail)
class ModelAdmin(admin.ModelAdmin):
    pass
