from django.urls import path
from django.views.generic import RedirectView

from .views import (DrugDetailView, DrugListView, ConditionDetailView, 
ConditionListView, InteractionDetailView, SearchView, ListContentsView)

urlpatterns = [
    path('drug/', DrugListView.as_view(), name='drug_list'),
    path('drug/<slug:slug>', DrugDetailView.as_view(), name='drug_detail'),
    path('condition/', ConditionListView.as_view(), name='condition_list'),
    path('condition/<slug:slug>', ConditionDetailView.as_view(), name='condition_detail'),
    path('interaction/<str:str>/<uuid:pk>', InteractionDetailView.as_view(), name='interaction_detail'),
    path('search/', SearchView, name='search'),
    path('interaction/', RedirectView.as_view(url='/search/')),
    path('list-contents/', ListContentsView, name='list-contents')
]
