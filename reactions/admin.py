from django.contrib import admin

from .models import DrugClass, Drug, Condition, Interaction, Source

# Register your models here.

class AbstractSaveAuthorModelAdmin(admin.ModelAdmin):
    '''Overrides save_model to set created_by and last_edited_by fields to request.user'''
    
    def save_model(self, request, obj, form, change):
        if obj.created_by == None: obj.created_by = request.user
        obj.last_edited_by = request.user
        super().save_model(request, obj, form, change)

class SourceAdmin(AbstractSaveAuthorModelAdmin):
    search_fields = ('name', 'publication')
    list_filter = ('created_by', 'last_edited_by')
    readonly_fields = ('created_by', 'last_edited_by')

class DrugClassAdmin(AbstractSaveAuthorModelAdmin):
    search_fields = ('name',)
    list_filter = ('created_by', 'last_edited_by')
    readonly_fields = ('created_by', 'last_edited_by')

class DrugAdmin(AbstractSaveAuthorModelAdmin):
    list_display = ('name', 'aliases', 'get_drug_classes')
    list_filter = ('created_by', 'last_edited_by')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('drug_class',)
    search_fields = ('name',)
    readonly_fields = ('created_by', 'last_edited_by')

    def get_queryset(self, request): # Prefetch many-many query
        qs = super().get_queryset(request)
        return qs.prefetch_related('drug_class')

class InteractionAdmin(AbstractSaveAuthorModelAdmin):
    list_display = ('name', 'get_condition_list', 'get_drug_list', 'ready_to_publish')
    list_editable = ('ready_to_publish',)
    list_filter = ('created_by', 'last_edited_by')
    filter_horizontal = ('conditions', 'drugs', 'sources')
    search_fields = ('name',)
    readonly_fields = ('created_by', 'last_edited_by')

    def get_queryset(self, request): # Prefetch many-many query
        qs = super().get_queryset(request)
        return qs.prefetch_related('conditions', 'drugs', 'sources')

class InteractionInline(admin.StackedInline):
    model = Interaction.conditions.through # Use intermediate table (for many-many relationship)
    extra = 1

class ConditionAdmin(AbstractSaveAuthorModelAdmin):
    list_display = ('name', 'aliases', 'ready_to_publish')
    list_editable = ('ready_to_publish',)
    list_filter = ('created_by', 'last_edited_by')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'aliases')
    readonly_fields = ('created_by', 'last_edited_by')
    inlines = [
        InteractionInline,
    ]

admin.site.register(DrugClass, DrugClassAdmin)
admin.site.register(Drug, DrugAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Interaction, InteractionAdmin)
admin.site.register(Source, SourceAdmin)