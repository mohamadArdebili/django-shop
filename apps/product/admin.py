from django.contrib import admin
from apps.product import models


class InformationAdmin(admin.StackedInline):
    model = models.Information


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "price"]
    inlines = [InformationAdmin]
    list_filter = ["size", "color", "price"]
    search_fields = ["title"]


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "slug", "parent"]
    prepopulated_fields = {"slug": ["title"]}


admin.site.register(models.Color)
admin.site.register(models.Size)
