from django.forms import ModelForm

from reactions.models import Interaction
from .models import ReviewSession, Review


class InteractionForReviewForm(ModelForm):
    '''
    Filters fields available in the Session CreateView
    '''
    class Meta:
        model = ReviewSession
        fields = ['interaction_reviews', 'host', 'open']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['interaction_reviews'].queryset = (
            Review.objects
            .filter(interaction__ready_for_peer_review=True)
            .exclude(interaction__peer_review_status='AC')  # Exclude accepted articles
            )
