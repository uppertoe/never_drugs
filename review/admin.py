from django.contrib import admin
from .models import Review, ReviewSession


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('condition', 'date_modified', 'actioned')
    list_editable = ('actioned',)
    list_filter = ('actioned',)
    exclude = ('update',)
    search_fields = ('condition',)
    readonly_fields = ('date_created', 'date_modified')


class ReviewSessionAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'host', 'open')
    list_editable = ('open',)
    list_filter = ('host',)
    filter_horizontal = ('reviews', 'user_list')
    readonly_fields = ('date_created', 'date_modified', 'last_ajax')


admin.site.register(Review, ReviewAdmin)
admin.site.register(ReviewSession, ReviewSessionAdmin)
