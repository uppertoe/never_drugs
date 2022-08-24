from django.contrib import admin

from .models import Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'actioned', 'for_review')
    list_editable = ('actioned', 'for_review')
    list_filter = ('actioned', 'created_by', 'last_edited_by')
    search_fields = ('name',)
    readonly_fields = ('name', 'created_by', 'last_edited_by')

    def save_model(self, request, obj, form, change):
        obj.last_edited_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Ticket, TicketAdmin)
