from django.contrib import admin

from .models import DrugClass, Drug, Condition, Interaction, Source
from .forms import InteractionAdminForm


class SaveAuthorMixin:
    '''
    Overrides save_model to set created_by
    and last_edited_by fields to request.user
    '''
    def save_model(self, request, obj, form, change):
        if obj.created_by is None:
            obj.created_by = request.user
        obj.last_edited_by = request.user
        super().save_model(request, obj, form, change)


class SourceAdmin(SaveAuthorMixin, admin.ModelAdmin):
    list_display = ('name', 'publication', 'year')
    search_fields = ('name', 'publication')
    list_filter = ('created_by', 'last_edited_by')
    readonly_fields = ('created_by', 'last_edited_by')


class DrugClassAdmin(SaveAuthorMixin, admin.ModelAdmin):
    search_fields = ('name',)
    list_filter = ('created_by', 'last_edited_by')
    readonly_fields = ('created_by', 'last_edited_by')


class DrugAdmin(SaveAuthorMixin, admin.ModelAdmin):
    list_display = ('name', 'aliases', 'get_drug_classes')
    list_filter = ('created_by', 'last_edited_by')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('drug_class',)
    search_fields = ('name',)
    readonly_fields = ('created_by', 'last_edited_by')

    def get_queryset(self, request):  # Prefetch many-many query
        qs = super().get_queryset(request)
        return qs.prefetch_related('drug_class')


class InteractionAdmin(SaveAuthorMixin, admin.ModelAdmin):
    form = InteractionAdminForm  # Extends field validation
    list_display = (
        'name',
        'get_condition_list',
        'get_drug_list',
        'ready_to_publish',
        'ready_for_peer_review')
    list_editable = ('ready_to_publish', 'ready_for_peer_review')
    list_filter = ('created_by', 'last_edited_by')
    filter_horizontal = (
        'conditions',
        'secondary_conditions',
        'drugs',
        'secondary_drugs',
        'sources')
    search_fields = ('name',)
    readonly_fields = ('created_by', 'last_edited_by', 'peer_review_status')

    def get_queryset(self, request):  # Prefetch many-many query
        qs = super().get_queryset(request)
        return qs.prefetch_related(
            'conditions',
            'secondary_conditions',
            'drugs',
            'secondary_drugs',
            'sources')


class ConditionAdmin(SaveAuthorMixin, admin.ModelAdmin):
    list_display = ('name', 'aliases', 'ready_to_publish')
    list_editable = ('ready_to_publish',)
    list_filter = ('created_by', 'last_edited_by')
    filter_horizontal = ('sources',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'aliases')
    readonly_fields = ('created_by', 'last_edited_by')


admin.site.register(DrugClass, DrugClassAdmin)
admin.site.register(Drug, DrugAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Interaction, InteractionAdmin)
admin.site.register(Source, SourceAdmin)
