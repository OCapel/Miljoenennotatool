from .models import Document, Category, Table

from django.contrib import admin


class DocumentAdmin(admin.ModelAdmin):
    readonly_fields = ('es_id', 'get_document',)


# Register your models here.
admin.site.register(Document, DocumentAdmin)
admin.site.register(Category)
admin.site.register(Table)