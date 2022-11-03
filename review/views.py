import uuid
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseBadRequest, JsonResponse, Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Review, ReviewSession
from .forms import InteractionForReviewForm


class SessionCreateView(CreateView):
    model = ReviewSession
    # fields = ['interaction_reviews', 'host', 'open']
    form_class = InteractionForReviewForm
    template_name = 'review/session_create.html'

    def get_success_url(self):
        return reverse('session_detail', kwargs={'pk': self.object.id})


class SessionListView(LoginRequiredMixin, ListView):
    model = ReviewSession
    context_object_name = 'session_list'
    template_name = 'review/session_list.html'
    queryset = ReviewSession.objects.all().prefetch_related(
        'interaction_reviews', 'user_list', 'host'
    )


def AjaxReviewDetailView(request):

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Forbidden'}, status=401)

    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponseBadRequest('Bad Request')

    if not request.method == 'GET':
        return JsonResponse({'status': 'Bad Request'}, status=400)

    id = request.GET.get('id')
    try:  # Verify that a valid UUID was passed
        id = uuid.UUID(id)
    except ValueError:
        raise Http404("Invalid resource identifier")

    session = get_object_or_404(ReviewSession, pk=id)
    context = {
        'interaction_reviews': Review.objects.filter(
            interaction_reviews=session
            ).prefetch_related('interaction')
    }
    return JsonResponse(
        {'html': render_to_string(
            'review/review_preview.html', {'session': context}
            )})


class SessionDetailView(DetailView):
    model = ReviewSession
    context_object_name = 'session'
    template_name = 'review/session_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = (
            self.object.interaction_reviews.all()
            .prefetch_related('interaction')
        )
        return context

    def get_object(self):
        # Associates the current user with the Review user_list
        obj = super().get_object()
        obj.user_list.add(self.request.user)
        return obj


class SessionEditView(UpdateView):
    model = ReviewSession
    context_object_name = 'session'
    template_name = 'review/session_edit.html'
    fields = ['interaction_reviews', 'open', 'host', 'user_list']


class ReviewListView(ListView):
    model = Review
    context_object_name = 'review_list'
    template_name = 'review/review_list.html'


class ReviewDetailView(DetailView):
    model = Review
    context_object_name = 'review'
    template_name = 'review/review_detail.html'
