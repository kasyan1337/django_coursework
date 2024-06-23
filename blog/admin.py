from django.contrib import admin

from .models import Blog


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date', 'views')
    search_fields = ('title',)
    readonly_fields = ('views',)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.views = 0  # Default value only on creation
        super().save_model(request, obj, form, change)
