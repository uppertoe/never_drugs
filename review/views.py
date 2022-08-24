import uuid
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponseBadRequest, JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from .models import Review, ReviewSession
from .forms import InteractionForReviewForm


class SessionCreateView(CreateView):
    model = ReviewSession
    # fields = ['interaction_reviews', 'host', 'open']
    form_class = InteractionForReviewForm
    template_name_suffix = '_create'


class SessionListView(ListView):
    model = ReviewSession
    context_object_name = 'session_list'
    template_name = 'review/session_list.html'
    queryset = ReviewSession.objects.all().prefetch_related(
        'interaction_reviews', 'user_list', 'host'
    )


def AjaxReviewDetailView(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    id = request.GET.get('id')
    try:  # Verify that a valid UUID was passed
        id = uuid.UUID(id)
    except ValueError:
        raise Http404("Invalid resource identifier")
    if is_ajax:
        if request.method == 'GET':
            session = get_object_or_404(ReviewSession, pk=id)
            context = {
                'interaction_reviews': Review.objects.filter(
                    interaction_reviews=session
                    ).prefetch_related('interaction')
            }
            return JsonResponse(
                {'html': render_to_string('review/review_preview.html', {'session': context})})
        return JsonResponse({'status': 'Bad Request'}, status=400)
    else:
        return HttpResponseBadRequest('Bad Request')


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
