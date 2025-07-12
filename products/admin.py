from django.contrib import admin
from .models import Product, Recipe, RecipeIngredient

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight', 'is_edible', 'energy', 'decay_time')
    search_fields = ('name',)
    list_filter = ('is_edible',)

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('product', 'output_quantity', 'craft_time')
    inlines = [RecipeIngredientInline]

@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'quantity')
    list_filter = ('recipe',)
