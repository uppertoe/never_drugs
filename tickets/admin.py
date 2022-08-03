from django.contrib import admin

from .models import Ticket

# Register your models here.
class TicketAdmin(admin.ModelAdmin):
    list_display = ('condition', 'drugs', 'actioned')
    list_editable = ('actioned',)
    list_filter = ('actioned', 'last_edited_by')
    search_fields = ('condition', 'drugs')
    readonly_fields = ('condition', 'drugs', 'created_by', 'last_edited_by')

    def save_model(self, request, obj, form, change):
        obj.last_edited_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Ticket, TicketAdmin)