from django.contrib import admin
from app import models

admin.site.register(models.Tag)
admin.site.register(models.Like)
admin.site.register(models.Comment)
admin.site.register(models.Post)
admin.site.register(models.Post_Tag)
