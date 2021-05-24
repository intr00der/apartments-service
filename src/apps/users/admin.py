from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    exclude = ('password', )


admin.site.register(User, UserAdmin)
