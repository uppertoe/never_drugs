from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from tickets.models import Ticket
from .models import Interaction


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = 'name', 'description'


class InteractionAdminForm(ModelForm):
    '''Implement validation for the InteractionAdmin'''
    class Meta():
        model = Interaction
        exclude = ()

    def clean(self):
        data = self.cleaned_data
        errors = []
        # Ensure that the same drug is not recorded in
        # self.drug and self.secondary_drug
        for secondary_drug in data['secondary_drugs']:
            if secondary_drug in data['drugs']:
                errors.append(ValidationError(
                    _('%(secondary_drug)s cannot be present in both \
                        the \'contraindicated drugs\' and \'drugs to \
                            use with caution\' lists'),
                    params={'secondary_drug': secondary_drug},))
        # Or self.condition and self.secondary_condition
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
