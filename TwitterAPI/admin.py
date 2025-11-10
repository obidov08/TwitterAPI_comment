from django.contrib import admin
from .models import (User, UserConfirmation, Post, Media, Comments)


admin.site.register([User, UserConfirmation, Post, Media, Comments])