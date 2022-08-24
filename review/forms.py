from django.forms import ModelForm

from reactions.models import Interaction
from .models import ReviewSession


class InteractionForReviewForm(ModelForm):
    class Meta:
        model = ReviewSession
        fields = ['interaction_reviews', 'host', 'open']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['interaction_reviews'].queryset = (
            Interaction.objects
            .filter(ready_for_peer_review=True)
            .exclude(peer_review_status='AC')  # Exclude accepted articles
            )
