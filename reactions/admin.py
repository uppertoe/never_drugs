from django.contrib import admin
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import DrugClass, Drug, Condition, Interaction, Source

# Register your models here.

class AbstractSaveAuthorModelAdmin(admin.ModelAdmin):
    '''Overrides save_model to set created_by and last_edited_by fields to request.user'''
    
    def save_model(self, request, obj, form, change):
        if obj.created_by == None: obj.created_by = request.user
        obj.last_edited_by = request.user
        super().save_model(request, obj, form, change)

class SourceAdmin(AbstractSaveAuthorModelAdmin):
    list_display = ('name', 'publication', 'year')
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

class InteractionAdminForm(ModelForm):
    '''Implement validation for the InteractionAdmin'''
    class Meta():
        model = Interaction
        exclude = ()
    
    def clean(self):
        data = self.cleaned_data
        errors = []
        # Ensure that the same drug is not recorded in self.drug and self.secondary_drug
        for secondary_drug in data['secondary_drugs']:
            if secondary_drug in data['drugs']:
                errors.append(ValidationError(
                    _('%(secondary_drug)s cannot be present in both the \'contraindicated drugs\' and \'drugs to use with caution\' lists'),
                    params={'secondary_drug': secondary_drug},))
        # Or self.condition and self.secondary_condition
        for secondary_condition in data['secondary_conditions']:
            if secondary_condition in data['conditions']:
                errors.append(ValidationError(
                    _('%(secondary_condition)s cannot be present in both the \'strongly linked\' and \'theoretically linked\' condition lists'),
                    params={'secondary_condition': secondary_condition},))
        if errors: raise ValidationError(errors)
        return data

class InteractionAdmin(AbstractSaveAuthorModelAdmin):
    form = InteractionAdminForm
    list_display = ('name', 'get_condition_list', 'get_drug_list', 'ready_to_publish')
    list_editable = ('ready_to_publish',)
    list_filter = ('created_by', 'last_edited_by')
    filter_horizontal = ('conditions', 'secondary_conditions', 'drugs', 'secondary_drugs', 'sources')
    search_fields = ('name',)
    readonly_fields = ('created_by', 'last_edited_by')

    def get_queryset(self, request): # Prefetch many-many query
        qs = super().get_queryset(request)
        return qs.prefetch_related('conditions', 'secondary_conditions', 'drugs', 'secondary_drugs', 'sources')

class ConditionAdmin(AbstractSaveAuthorModelAdmin):
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