from django.contrib import admin

from account import models

admin.site.register(models.Month)
admin.site.register(models.UserProfile)