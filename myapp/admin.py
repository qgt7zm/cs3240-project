from django.contrib import admin

from myapp import models

admin.site.register(models.SiteUser)
admin.site.register(models.UserFile)
admin.site.register(models.ReportForm)
