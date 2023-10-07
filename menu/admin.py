from django.contrib import admin
from .models import MenuItem


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    list_filter = ('parent', )
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(MenuItem, MenuItemAdmin)
