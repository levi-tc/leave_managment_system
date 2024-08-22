from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from stores.models import StoreEmployee

class StoreInline(admin.TabularInline):
    model = StoreEmployee
    extra = 1

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'user_type', 'get_store', 'is_staff']
    inlines = [StoreInline]
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('user_type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('user_type',)}),
    )

    def get_store(self, obj):
        return obj.get_store()
    get_store.short_description = 'Store'

admin.site.register(CustomUser, CustomUserAdmin)