from django.views.generic import ListView, DetailView

from .models import Review, ReviewSession


class SessionListView(ListView):
    model = ReviewSession
    context_object_name = 'session_list'
    template_name = 'review/session_list.html'


class SessionDetailView(DetailView):
    model = ReviewSession
    context_object_name = 'session'
    template_name = 'review/session_detail'


class ReviewListView(ListView):
    model = Review
    context_object_name = 'review_list'
    template_name = 'review/review_list.html'


class ReviewDetailView(DetailView):
    model = Review
    context_object_name = 'review'
    template_name = 'review/review_detail.html'
