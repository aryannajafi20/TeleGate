from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import User
from accounts.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'is_staff', 'is_admin', 'is_developer', 'is_superuser')
    list_filter = ('is_admin', 'is_developer', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ()

    # ← اضافه کن:
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_superuser', 'is_developer')}),
        # تاریخ‌ها در readonly_fields قرار دارند، لذا نمایش‌شان مشکلی ندارد
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # هنگام افزودن کاربر جدید نباید فیلدهای readonly را قرار بدی
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_admin', 'is_superuser', 'is_developer'),
        }),
    )

    # ... بقیه متدها و actions ...

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)