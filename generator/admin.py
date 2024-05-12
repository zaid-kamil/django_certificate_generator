from django.contrib import admin
from .models import Dataset, Certificate, Report
# Register your models here.

admin.site.register(Dataset)
admin.site.register(Certificate)
admin.site.register(Report)