from django.contrib import admin

from .models import DrugClass, Drug, Condition, Interaction, Source

# Register your models here.

class SourceAdmin(admin.ModelAdmin):
    search_fields = ('name', 'publication')

class DrugClassAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'aliases', 'get_drug_classes')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('drug_class',)
    search_fields = ('name',)

    def get_queryset(self, request): # Prefetch many-many query
        qs = super().get_queryset(request)
        return qs.prefetch_related('drug_class')

class InteractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_condition_list', 'get_drug_list', 'ready_to_publish')
    list_editable = ('ready_to_publish',)
    filter_horizontal = ('conditions', 'drugs', 'sources')
    search_fields = ('name',)

    def get_queryset(self, request): # Prefetch many-many query
        qs = super().get_queryset(request)
        return qs.prefetch_related('conditions', 'drugs', 'sources')

class InteractionInline(admin.StackedInline):
    model = Interaction.conditions.through # Use intermediate table (for many-many relationship)
    extra = 1

class ConditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'aliases', 'ready_to_publish')
    list_editable = ('ready_to_publish',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'aliases')
    inlines = [
        InteractionInline,
    ]

admin.site.register(DrugClass, DrugClassAdmin)
admin.site.register(Drug, DrugAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Interaction, InteractionAdmin)
admin.site.register(Source, SourceAdmin)