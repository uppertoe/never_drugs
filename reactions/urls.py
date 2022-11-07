from django.urls import path
from django.views.generic import RedirectView
from django.views.decorators.cache import cache_page

from .views import (
    DrugDetailView, DrugListView, ConditionDetailView,
    ConditionListView, InteractionDetailView,
    search_view, list_contents_view)

urlpatterns = [
    path(
        'drug/',
        DrugListView.as_view(),
        name='drug_list'),
    path(
        'drug/<slug:slug>',
        DrugDetailView.as_view(),
        name='drug_detail'),
    path(
        'condition/',
        ConditionListView.as_view(),
        name='condition_list'),
    path(
        'condition/<slug:slug>',
        ConditionDetailView.as_view(),
        name='condition_detail'),
    path(
        # <str:str> populated from query but not required for path
        'interaction/<str:str>/<uuid:pk>',
        InteractionDetailView.as_view(),
        name='interaction_detail'),
    path(
        'search/',
        search_view,
        name='search'),
    path(
        'interaction/',
        RedirectView.as_view(url='/search/')),
    path(
        # AJAX operation for URL-specific per-view cache
        'list-contents/',
        cache_page(60 * 15)(list_contents_view),
        name='list-contents')]
