import uuid
import json
import datetime
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.http import HttpResponseBadRequest, JsonResponse, Http404
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils.html import escape
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


def ajax_review_detail_view(request):

    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponseBadRequest('Bad Request')

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Forbidden'}, status=401)

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
    '''
    Displays the Session from which users can select Reviews
    '''

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
        # Associates the current user with the Review.user_list
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


class ReviewDetailView(LoginRequiredMixin, DetailView):
    model = Review
    context_object_name = 'review'
    current_session_id = None

    def get(self, request, *args, **kwargs):
        # Check whether a valid UUID was passed
        session_id = request.GET.get('session_id')
        if session_id:
            try:
                self.current_session_id = uuid.UUID(session_id)
            except ValueError:
                print(f'Invalid UUID provided in GET: {session_id}')
        return super().get(self, request, *args, **kwargs)

    def get_template_names(self):
        '''
        Finds all ReviewSessions associated with the current review
        Compares the GET provided current_session_id with these to
        find the host for the current session
        Allocates host or non-host template accordingly
        '''
        session_id_dict = {}
        for session in self.object.interaction_reviews.all():
            session_id_dict.update({session.id: session.host})
        session_host = session_id_dict.get(self.current_session_id, '')
        if self.request.user == session_host:
            return ['review/review_host_detail.html']
        return ['review/review_detail.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the referring ReviewSession to the context
        if self.current_session_id:  # TRUE if is valid UUID
            try:
                review_session = ReviewSession.objects.get(
                    id=self.current_session_id)
                context['review_session'] = review_session
            except ReviewSession.DoesNotExist:
                message = 'No match for ReviewSession GET parameter'
                print(f'{message}: {self.current_session_id}')
        return context


def ajax_check_last_update(request):
    '''
    Returns the last_ajax (DateTime) value for a given session_id
    '''
    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponseBadRequest('Bad Request')

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Forbidden'}, status=401)

    if not request.method == 'POST':
        return JsonResponse({'status': 'Bad Request'}, status=400)

    # Look up the ReviewSession
    session_pk = request.GET.get("session_id")
    current_session = get_object_or_404(ReviewSession, session_pk)

    # Supply the last_ajax result
    return JsonResponse({'last_ajax': current_session.last_ajax}, status=200)


def ajax_active_review_session(request):

    '''
    GET: shows the latest update to the selected review
    POST: updates the Review.update

    Requires:
    - User
    - ReviewSession ID
    - Review ID

    Pre-requisites:
    - User is logged in
    - Request is ajax
    - User is host (if POST)
    - Review is in ReviewSession (if POST)
    '''

    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponseBadRequest('Bad Request')

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Forbidden'}, status=401)

    if request.method == 'GET':
        # Retrieve the result from Review.update
        review_pk = request.GET.get("review_id")
        current_review = get_object_or_404(Review, review_pk)
        return JsonResponse({'update': current_review.update}, status=200)

    if request.method == 'POST':
        # Look up the ReviewSession
        session_pk = request.POST.get("session_id")
        current_session = get_object_or_404(ReviewSession, session_pk)

        # Check whether the current user is host
        if not request.user == current_session.host:
            return JsonResponse({'status': 'Forbidden'}, status=401)

        # Determine the Review to be updated
        review_pk = request.POST.get("review_id")
        review = get_object_or_404(Review, review_pk)

        # Check whether the Review is in the current ReviewSession
        if review not in current_session.interaction_reviews:
            return JsonResponse({'status': 'Forbidden'}, status=401)

        # Store the result in Review.update
        review.update = request.POST.get("update")
        review.last_ajax = datetime.datetime.now()
        review.save()
        return JsonResponse({'status': 'Update Successful'}, status=200)

    return JsonResponse({'status': 'Bad Request'}, status=400)


def ajax_save_review_session(request):
    '''
    'Saves' the input to the review

    Requires:
    - User
    - ReviewSession ID
    - Review ID

    Pre-requisites:
    - User is logged in
    - Request is ajax
    - User is host
    - Review is in ReviewSession

    Sets the Review.comment to Review.update
    '''
    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponseBadRequest('Bad Request')

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Forbidden'}, status=401)

    if request.method == 'POST':
        # Unpack the AJAX JSON
        data = json.load(request)

        # Look up the ReviewSession
        session_id = data.get("session_id")
        current_session = get_object_or_404(ReviewSession, id=session_id)

        # Check whether the current user is host
        if not request.user == current_session.host:
            return JsonResponse({'status': 'Forbidden'}, status=401)

        # Determine the Review to be updated
        review_id = data.get("review_id")
        review = get_object_or_404(Review, id=review_id)

        # Check whether the Review is in the current ReviewSession
        if review not in current_session.interaction_reviews.all():
            return JsonResponse({'status': 'Forbidden'}, status=401)

        # Ensure the review.update is current
        latest_comment = data.get("latest_comment")
        review.update = latest_comment
        review.last_ajax = datetime.datetime.now()

        # Replace the comment with the updated comment
        review.comment = latest_comment
        review.save()
        response = {
            'status': 'Save Successful',
            'latest_comment_html': render_to_string(
                'review/review_revert_text.html',
                {'review': review}),
            'latest_comment': latest_comment,
        }
        return JsonResponse(response, status=200)

    return JsonResponse({'status': 'Bad Request'}, status=400)


def ajax_revert_review(request):

    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponseBadRequest('Bad Request')

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Forbidden'}, status=401)

    if request.method == 'POST':
        # Unpack the AJAX JSON
        data = json.load(request)

        # Look up the ReviewSession
        session_id = data.get("session_id")
        current_session = get_object_or_404(ReviewSession, id=session_id)

        # Check whether the current user is host
        if not request.user == current_session.host:
            return JsonResponse({'status': 'Forbidden'}, status=401)

        # Determine the Review to be updated
        review_id = data.get("review_id")
        review = get_object_or_404(Review, id=review_id)

        # Check whether the Review is in the current ReviewSession
        if review not in current_session.interaction_reviews.all():
            return JsonResponse({'status': 'Forbidden'}, status=401)

        # Revert the Review.update to the saved Review.comment
        review.update = review.comment
        review.last_ajax = datetime.datetime.now()
        review.save()
        response = {
            'status': 'Revert Successful',
            'latest_comment_html': render_to_string(
                'review/review_revert_text.html',
                {'review': review}),
            'latest_comment': review.update,
        }
        return JsonResponse(response, status=200)

    return JsonResponse({'status': 'Bad Request'}, status=400)


def ajax_auto_update_review(request):

    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponseBadRequest('Bad Request')

    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Forbidden'}, status=401)

    if request.method == 'GET':
        review_id = request.GET.get("review_id")
        review = get_object_or_404(Review, id=review_id)

        latest_comment_markdown = review.update_markdown()
        return JsonResponse({
            'status': 'Retrieval Successful',
            'latest_comment_html': latest_comment_markdown
        })

    if request.method == 'POST':
        # Unpack the AJAX JSON
        data = json.load(request)

        # Look up the ReviewSession
        session_id = data.get("session_id")
        current_session = get_object_or_404(ReviewSession, id=session_id)

        # Check whether the current user is host
        if not request.user == current_session.host:
            return JsonResponse({'status': 'Forbidden'}, status=401)

        # Determine the Review to be updated
        review_id = data.get("review_id")
        review = get_object_or_404(Review, id=review_id)

        # Check whether the Review is in the current ReviewSession
        if review not in current_session.interaction_reviews.all():
            return JsonResponse({'status': 'Forbidden'}, status=401)

        # Ensure the review.update is current
        latest_comment = data.get("latest_comment")
        review.update = latest_comment
        review.last_ajax = datetime.datetime.now()
        review.save()
        response = {
            'status': 'Update Successful',
            'latest_comment_html': render_to_string(
                'review/review_revert_text.html',
                {'review': review}),
            'latest_comment': latest_comment,
        }
        return JsonResponse(response, status=200)

    return JsonResponse({'status': 'Bad Request'}, status=400)