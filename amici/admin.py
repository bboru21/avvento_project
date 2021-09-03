from django.contrib import admin

from .models import (
    Friend,
    FriendList
)

admin.site.register(Friend)
admin.site.register(FriendList)