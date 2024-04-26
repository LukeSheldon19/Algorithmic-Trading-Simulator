from django.contrib import admin

from .models import Profile, Status, Poke

admin.site.register(Profile)
admin.site.register(Status)
admin.site.register(Poke)
