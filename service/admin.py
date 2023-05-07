from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
from .models import ServiceUser, Restaurant, RestAddresses, WorkingHours, MenuDish, Vote


class ServiceUserAdmin(UserAdmin):
    fieldsets = (
        (_("Unique"), {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone_number", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
    list_display = ("username", "phone_number", "email", "first_name", "last_name", "is_staff")
    search_fields = ("username", "first_name", "last_name", "phone_number", "email")


admin.site.register(ServiceUser, ServiceUserAdmin)
admin.site.register(Restaurant)
admin.site.register(RestAddresses)
admin.site.register(WorkingHours)
admin.site.register(MenuDish)
admin.site.register(Vote)
