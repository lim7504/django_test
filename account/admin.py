from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from account.models import ExtendUser
# from account.models import Certificate

class ExtendUserInline(admin.StackedInline):
    model = ExtendUser
    can_delete = False
    verbose_name_plural = 'extenduser'

class UserAdmin(BaseUserAdmin):
    inlines = (ExtendUserInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# admin.site.register(Certificate)