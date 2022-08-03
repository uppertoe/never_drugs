from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Ticket

# Create your views here.
class TicketListView(ListView):
    queryset = Ticket.objects.filter(actioned=False)
    context_object_name = 'ticket_list'
    template_name = 'tickets/ticket_list.html'

class TicketDetailView(DetailView):
    model = Ticket
    context_object_name = 'ticket'
    template_name = 'tickets/ticket_detail.html'

class CreateTicketView(TemplateView):
    template_name = 'tickets/create_ticket.html'