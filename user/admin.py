from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Inventory, ProductionExpertise

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Economy Info', {
            'fields': ('money', 'max_carry_weight')
        }),
    )
    list_display = ('username', 'email', 'money', 'max_carry_weight', 'is_staff')

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity')
    list_filter = ('product',)
    search_fields = ('user__username',)

@admin.register(ProductionExpertise)
class ProductionExpertiseAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'level', 'xp')
    list_filter = ('product',)
    search_fields = ('user__username',)
