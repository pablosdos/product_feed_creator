from django.contrib import admin

from .models import Feed, Serverkast_Product, TopSystemsProduct

class ServerkastProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'is_selected')

class TopSystemsProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'is_selected')

admin.site.register(Feed)
admin.site.register(Serverkast_Product, ServerkastProductAdmin)
admin.site.register(TopSystemsProduct, TopSystemsProductAdmin)