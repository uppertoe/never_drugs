from django.contrib import admin

from .models import DrugClass, Drug, Condition, Interaction

# Register your models here.

class DrugClassAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'aliases', 'get_drug_classes')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('drug_class',)
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('drug_class')

class InteractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_condition_list', 'get_drug_list')
    filter_horizontal = ('conditions', 'drugs')
    search_fields = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('conditions', 'drugs')

class InteractionInline(admin.StackedInline):
    model = Interaction.conditions.through
    extra = 1

class ConditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'aliases')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'aliases')
    inlines = [
        InteractionInline,
    ]

admin.site.register(DrugClass, DrugClassAdmin)
admin.site.register(Drug, DrugAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Interaction, InteractionAdmin)