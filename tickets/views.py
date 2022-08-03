from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

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

class TicketCreateView(CreateView):
    model = Ticket
    fields = 'condition', 'drugs', 'description'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)

class TicketUpdateView(UpdateView):
    model = Ticket
    fields = 'condition', 'drugs', 'description'

class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('ticket-list')