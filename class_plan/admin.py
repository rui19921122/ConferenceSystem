from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.ClassPlanBase, models.ClassPlanDayDetail, models.SingleClaimDetail, models.ClassPlanDayTable,
                models.SinglePublishDetail, models.WhichDepartmentCanEditClassPlan)
class ModelAdmin(admin.ModelAdmin):
    pass
