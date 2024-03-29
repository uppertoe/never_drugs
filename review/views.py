import uuid
import json
import datetime
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import RedirectView
from django.http import HttpResponseBadRequest, JsonResponse, Http404
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Review, ReviewSession
from .forms import InteractionForReviewForm, ConditionPeerReviewStatusForm


class SessionCreateView(PermissionRequiredMixin, CreateView):
    model = ReviewSession
    form_class = InteractionForReviewForm
    template_name = 'review/session_create.html'
    permission_required = 'accounts.access_peer_review'

    def get_success_url(self):
        return reverse_lazy('session_detail', kwargs={'pk': self.object.id})


class SessionListView(PermissionRequiredMixin, ListView):
    model = ReviewSession
    context_object_name = 'session_list'
    template_name = 'review/session_list.html'
    permission_required = 'accounts.access_peer_review'
    queryset = (
        ReviewSession.objects.all()
        .order_by('-date_created')
        .prefetch_related('reviews', 'user_list', 'host'))


class SessionLatestView(PermissionRequiredMixin, RedirectView):
    # Redirect to the last created ReviewSession
    permanent = False
    query_string = False
    permission_required = 'accounts.access_peer_review'

    def get_redirect_url(self, *args, **kwargs):
        session = ReviewSession.objects.all().order_by('-date_created').first()
        if not session:
            raise Http404
        return session.get_absolute_url()


def ajax_review_detail_view(request):

    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponseBadRequest('Bad Request')

    if not request.user.has_perm('accounts.access_peer_review'):
        return JsonResponse({'status': 'Forbidden'}, status=401)

    if not request.method == 'GET':
        return JsonResponse({'status': 'Bad Request'}, status=400)

    id = request.GET.get('id')
    try:  # Verify that a valid UUID was passed
        id = uuid.UUID(id)
    except ValueError:
        raise Http404("Invalid resource identifier")

    session = get_object_or_404(ReviewSession, pk=id)
    # Find the other reviews associated with this ReviewSession
    associated_reviews = Review.objects.filter(
        reviews=session
        ).prefetch_related('condition')
    context = associated_reviews

    # Render to HTML
    html = render_to_string(
        'review/fragments/review_preview.html',
        {'review_list': context, 'session': session})
    return JsonResponse({'html': html})


class SessionDetailView(PermissionRequiredMixin, DetailView):
    '''
    Displays the Session from which users can select Reviews
    '''

    model = ReviewSession
    context_object_name = 'session'
    template_name = 'review/session_detail.html'
    permission_required = 'accounts.access_peer_review'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = (
            self.object.reviews.all()
            .prefetch_related('condition')
        )
        return context

    def get_object(self):
        # Associates the current user with the ReviewSession.user_list
        obj = super().get_object()
        if obj.open:
            obj.user_list.add(self.request.user)
        return obj


class SessionEditView(PermissionRequiredMixin, UpdateView):
    model = ReviewSession
    context_object_name = 'session'
    template_name = 'review/session_edit.html'
    fields = ['reviews', 'open', 'host', 'user_list']
    permission_required = 'accounts.access_peer_review'


class ReviewListView(PermissionRequiredMixin, ListView):
    model = Review
    context_object_name = 'review_list'
    template_name = 'review/review_list.html'
    permission_required = 'accounts.access_peer_review'


class ReviewDetailView(PermissionRequiredMixin, DetailView):
    # Call get_form() in get_context_data to provide initial values
    # form.save() is handled in ajax_save_review_session()
    model = Review
    context_object_name = 'review'
    current_session_id = None
    form_class = ConditionPeerReviewStatusForm
    permission_required = 'accounts.access_peer_review'

    def get(self, request, *args, **kwargs):
        # Check whether a valid UUID was passed
        session_id = request.GET.get('session_id')
        if session_id:
            try:
                self.current_session_id = uuid.UUID(session_id)
            except ValueError:
                print(f'Invalid UUID provided in GET: {session_id}')
        return super().get(self, request, *args, **kwargs)

    def get_form(self):
        # Ensure that a new Condition is not created
        if self.object.condition:
            form = self.form_class(instance=self.object.condition)
            return form
        return print(f'Error: no associated condition for review {self.object}')

    def get_template_names(self):
        '''
        Finds all ReviewSessions associated with the current review
        Compares the GET provided current_session_id with these to
        find the host for the current session
        Allocates host or non-host template accordingly
        '''
        session_id_dict = {}
        for session in self.object.reviews.all():
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
        # Add the form to the context
        context['peer_review_form'] = self.get_form()
        return context


def ajax_save_review_session(request):
    '''
    Sets the Review.comment to Review.update
    Requires:
    - User
    - ReviewSession ID
    - Review ID
    '''
    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponseBadRequest('Bad Request')

    if not request.user.has_perm('accounts.access_peer_review'):
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
        if review not in current_session.reviews.all():
            return JsonResponse({'status': 'Forbidden'}, status=401)

        # Ensure the review.update is current
        latest_comment = data.get("latest_comment")
        review.update = latest_comment
        review.last_ajax = datetime.datetime.now()

        # Update (but do not create) the peer review status
        if review.condition:
            peer_review_form = data.get("peer_review_form")
            form = ConditionPeerReviewStatusForm(
                {'peer_review_status': peer_review_form},
                instance=review.condition,
                )
            form.save()

        # Replace the comment with the updated comment
        review.comment = latest_comment
        review.save()
        response = {
            'status': 'Save Successful',
            'latest_comment_html': render_to_string(
                'review/fragments/review_revert_text.html',
                {'review': review}),
            'latest_comment': latest_comment,
        }
        return JsonResponse(response, status=200)
    return JsonResponse({'status': 'Bad Request'}, status=400)


def ajax_revert_review(request):

    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponseBadRequest('Bad Request')

    if not request.user.has_perm('accounts.access_peer_review'):
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
        if review not in current_session.reviews.all():
            return JsonResponse({'status': 'Forbidden'}, status=401)

        # Revert the Review.update to the saved Review.comment
        review.update = review.comment
        review.last_ajax = datetime.datetime.now()
        review.save()
        html = render_to_string(
            'review/fragments/review_revert_text.html',
            {'review': review}
            )
        response = {
            'status': 'Revert Successful',
            'latest_comment_html': html,
            'latest_comment': review.update,
        }
        return JsonResponse(response, status=200)
    return JsonResponse({'status': 'Bad Request'}, status=400)


def ajax_auto_update_review(request):

    def update_user_list(session_id):
        # If a session_id is available, return an HTML user_list
        if session_id:
            session = get_object_or_404(ReviewSession, id=session_id)
            html = render_to_string(
                'review/fragments/review_users.html',
                {'review_session': session})
            return html
        return None

    if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        return HttpResponseBadRequest('Bad Request')

    if not request.user.has_perm('accounts.access_peer_review'):
        return JsonResponse({'status': 'Forbidden'}, status=401)

    if request.method == 'GET':
        review_id = request.GET.get("review_id")
        session_id = request.GET.get("session_id")
        review = get_object_or_404(Review, id=review_id)
        latest_comment_markdown = review.update_markdown()
        revert_text_html = render_to_string(
            'review/fragments/review_revert_text.html',
            {'review': review}
            )
        response = {
            'status': 'Retrieval Successful',
            'latest_comment_html': latest_comment_markdown,
            'revert_text_html': revert_text_html,
            'user_list_html': update_user_list(session_id),
            'peer_review_status': review.condition.get_peer_review_status_display()
            }
        return JsonResponse(response, status=200)

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
        if review not in current_session.reviews.all():
            return JsonResponse({'status': 'Forbidden'}, status=401)

        # Ensure the review.update is current
        latest_comment = data.get("latest_comment")
        review.update = latest_comment
        review.last_ajax = datetime.datetime.now()
        review.save()
        html = render_to_string(
            'review/fragments/review_revert_text.html',
            {'review': review}
            )
        response = {
            'status': 'Update Successful',
            'latest_comment_html': html,
            'latest_comment': latest_comment,
            'user_list_html': update_user_list(session_id),
        }
        return JsonResponse(response, status=200)
    return JsonResponse({'status': 'Bad Request'}, status=400)
