from django.contrib import admin
from users.models import User, Follower

admin.site.register(User)
admin.site.register(Follower)
