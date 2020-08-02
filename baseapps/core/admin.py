from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class AppUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('username', 'is_staff', 'is_active',)
    list_filter = ('username', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'username','role',
                           'password', 'alamat', 'phone', 'nama', 'birth_date', 'avatar')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','nama','is_staff', 'is_active', 'password1', 'password2', )}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(User, AppUserAdmin)
admin.site.site_title = "services KUB"
admin.site.site_header = "KUB database administration"
admin.site.index_title = "KUB"
