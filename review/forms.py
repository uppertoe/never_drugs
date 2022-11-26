from django import forms

from .models import ReviewSession, Review


class InteractionForReviewForm(forms.ModelForm):
    '''
    Filters fields available in the Session CreateView
    '''
    class Meta:
        model = ReviewSession
        fields = ['reviews', 'host', 'open']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reviews'].queryset = (
            Review.objects  # Exclude accepted articles
            .filter(condition__ready_for_peer_review=True)
            .exclude(condition__peer_review_status='AC')
            .exclude(actioned=True)
            )
