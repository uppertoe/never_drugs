from django.urls import path
from .views import CreateTicketView, TicketDetailView, TicketListView

urlpatterns = [
    path('create/', CreateTicketView.as_view(), name='create_ticket'),
    path('<uuid:pk>', TicketDetailView.as_view(), name='ticket_detail'),
    path('', TicketListView.as_view(), name='ticket_list')
]