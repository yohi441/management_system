from django.contrib import admin
from management_system import models



admin.site.register(models.Client)
admin.site.register(models.Category)
admin.site.register(models.Item)
admin.site.register(models.Transaction)
admin.site.register(models.Forfeit)
