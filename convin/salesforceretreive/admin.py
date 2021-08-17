from django.contrib import admin

# Register your models here.
from .models import SalesforceAuth,UserData

admin.site.register(SalesforceAuth)
admin.site.register(UserData)