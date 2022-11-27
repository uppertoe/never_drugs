from django.urls import path

from .views import (
    SessionListView,
    SessionDetailView,
    ReviewListView,
    ReviewDetailView,
    SessionCreateView,
    SessionLatestView,
    SessionEditView,
    ajax_save_review_session,
    ajax_revert_review,
    ajax_auto_update_review,
    ajax_review_detail_view,
    )

urlpatterns = [
    path('', ReviewListView.as_view(), name='review_list'),
    path('<uuid:pk>', ReviewDetailView.as_view(), name='review_detail'),
    path('session/', SessionListView.as_view(), name='session_list'),
    path('session/<uuid:pk>', SessionDetailView.as_view(), name='session_detail'),
    path('session/start', SessionCreateView.as_view(), name='session_create'),
    path('session/edit/<uuid:pk>', SessionEditView.as_view(), name='session_edit'),
    path('session/latest', SessionLatestView.as_view(), name='session_latest'),
    path('ajax/session', ajax_review_detail_view, name='ajax_review_detail'),
    path('ajax/save', ajax_save_review_session, name='ajax-save-review'),
    path('ajax/revert', ajax_revert_review, name='ajax-revert-review'),
    path('ajax/update', ajax_auto_update_review, name='ajax-update-review'),
    ]
