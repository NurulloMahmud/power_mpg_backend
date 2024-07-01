from django.contrib import admin
from .models import Company, CustomUser, CompanyStatus


admin.site.register(Company)
admin.site.register(CustomUser)
admin.site.register(CompanyStatus)