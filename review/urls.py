from django.urls import path

from .views import (
    SessionListView, SessionDetailView, ReviewListView,
    ReviewDetailView)

urlpatterns = [
    path(
        'session/',
        SessionListView.as_view(),
        name='session_list'),
    path(
        'session/<uuid:pk>',
        SessionDetailView.as_view(),
        name='session_detail'),
    path(
        '',
        ReviewListView.as_view(),
        name='review_list'),
    path(
        '<uuid:pk>',
        ReviewDetailView.as_view(),
        name='review_detail')]
