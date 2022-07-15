from django.contrib import admin

from .models import DrugClass, Drug, Condition, Interaction

# Register your models here.

class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'aliases')
    prepopulated_fields = {'slug': ('name',)}

class ConditionAdmin(admin.ModelAdmin):
    list_display = ('name', 'aliases')
    prepopulated_fields = {'slug': ('name',)}

class InteractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'severity', 'evidence')
    filter_horizontal = ('conditions', 'drugs')

admin.site.register(DrugClass)
admin.site.register(Drug, DrugAdmin)
admin.site.register(Condition, ConditionAdmin)
admin.site.register(Interaction, InteractionAdmin)