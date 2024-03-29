from django.urls import path
from django.views.generic import RedirectView

from .views import (
    DrugDetailView, DrugListView, ConditionDetailView,
    ConditionListView, InteractionDetailView,
    search_view, list_contents_view)

urlpatterns = [
    path(
        'drugs/',
        DrugListView.as_view(),
        name='drug_list'),
    path(
        'drugs/<slug:slug>',
        DrugDetailView.as_view(),
        name='drug_detail'),
    path(
        'conditions/',
        ConditionListView.as_view(),
        name='condition_list'),
    path(
        'conditions/<slug:slug>',
        ConditionDetailView.as_view(),
        name='condition_detail'),
    path(
        # <str:str> populated from query but not required for path
        'interactions/<str:str>/<uuid:pk>',
        InteractionDetailView.as_view(),
        name='interaction_detail'),
    path(
        'search/',
        search_view,
        name='search'),
    path(
        'interactions/',
        RedirectView.as_view(url='/search/')),
    path(
        # AJAX operation for URL-specific per-view cache
        'list-contents/',
        list_contents_view,
        name='list-contents')]
