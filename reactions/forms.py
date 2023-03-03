from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from markdownx.widgets import MarkdownxWidget

from tickets.models import Ticket
from .models import Interaction, Condition, Drug


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = 'name', 'description'


class DrugAdminForm(ModelForm):
    class Meta:
        model = Drug
        exclude = ()
        widgets = {
            'description': MarkdownxWidget(attrs={'rows': 20, 'cols': 120})
        }


class InteractionAdminForm(ModelForm):
    '''Implement validation for the InteractionAdmin'''
    class Meta:
        model = Interaction
        exclude = ()
        widgets = {
            'description': MarkdownxWidget(attrs={'rows': 40, 'cols': 120})
        }

    def clean(self):
        data = self.cleaned_data
        errors = []
        # Ensure that the same drug is not recorded in
        # self.drug and self.secondary_drug
        if data.get('drugs'):
            for secondary_drug in data['secondary_drugs']:
                if secondary_drug in data['drugs']:
                    errors.append(ValidationError(
                        _('%(secondary_drug)s cannot be present in both \
                            the \'contraindicated drugs\' and \'drugs to \
                                use with caution\' lists'),
                        params={'secondary_drug': secondary_drug},))
        # Or self.condition and self.secondary_condition
        if data.get('conditions'):
            for secondary_condition in data['secondary_conditions']:
                if secondary_condition in data['conditions']:
                    errors.append(ValidationError(
                        _('%(secondary_condition)s cannot be present in both \
                            the \'strongly linked\' and \'theoretically linked\' \
                                condition lists'),
                        params={'secondary_condition': secondary_condition},))
        if errors:
            raise ValidationError(errors)
        return data


class ConditionAdminForm(ModelForm):
    class Meta:
        model = Condition
        fields = '__all__'
        widgets = {
            'description': MarkdownxWidget(attrs={'rows': 40, 'cols': 120})
        }
