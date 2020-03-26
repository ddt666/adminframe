from django.contrib import admin
from rbac import models


# Register your models here.

class MenuAdmin(admin.ModelAdmin):
    list_display = ["title", "icon", "weight"]
    list_editable = ["icon", "weight"]


class PermissionAdmin(admin.ModelAdmin):
    list_display = ["title", "url", "menu", "is_menu", "parent", "alias"]
    list_editable = ["url", "menu", "is_menu", "parent", "alias"]


admin.site.register(models.Role)
admin.site.register(models.Permission,PermissionAdmin)
admin.site.register(models.Menu, MenuAdmin)
