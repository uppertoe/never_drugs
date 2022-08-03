from django.urls import path
from .views import (TicketCreateView, TicketUpdateView, TicketDeleteView,
 TicketDetailView, TicketListView)

urlpatterns = [
    path('create/', TicketCreateView.as_view(), name='ticket-create'),
    path('<uuid:pk>', TicketUpdateView.as_view(), name='ticket-update'),
    path('<uuid:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
    path('review/<uuid:pk>', TicketDetailView.as_view(), name='ticket-detail'),
    path('review/', TicketListView.as_view(), name='ticket-list')
]