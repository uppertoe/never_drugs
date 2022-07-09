from django.urls import path

from .views import (DrugDetailView, DrugListView, ConditionDetailView, 
ConditionListView, InteractionDetailView, InteractionListView)

urlpatterns = [
    path('drug/', DrugListView.as_view(), name='drug_list'),
    path('drug/<slug:slug>', DrugDetailView.as_view(), name='drug_detail'),
    path('condition/', ConditionListView.as_view(), name='condition_list'),
    path('condition/<slug:slug>', ConditionDetailView.as_view(), name='condition_detail'),
    path('interaction/', InteractionListView.as_view(), name='interaction_list'),
    path('interaction/<str:str>/<uuid:pk>', InteractionDetailView.as_view(), name='interaction_detail'),
]
