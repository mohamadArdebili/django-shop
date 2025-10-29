from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from apps.account.models import User, Otp
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["phone", "email", "is_admin"]
    list_filter = ["phone", "is_admin"]
    # Fields related to editing an existing user
    fieldsets = [
        (None, {"fields": ["phone", "email", "password"]}),
        ("Personal info", {"fields": ["full_name"]}),
        ("Permissions", {"fields": ["is_admin", "is_active"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    # Fields related to creating a user
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["phone", "email", "full_name", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", "phone"]
    ordering = ["email"]
    filter_horizontal = []


admin.site.register(User, UserAdmin)
admin.site.register(Otp)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
