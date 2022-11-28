from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from core.utilities import JsonableResponseMixin
from .models import Ticket


class TicketListView(LoginRequiredMixin, ListView):
    context_object_name = 'ticket_list'
    template_name = 'tickets/ticket_list.html'

    def get_queryset(self):
        return Ticket.objects.filter(created_by=self.request.user)

    def get_context_data(self, **kwargs):
        '''Add all tickets to the context for superusers'''
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context['all_tickets'] = Ticket.objects.filter(actioned=False)
        return context


class TicketCreateView(JsonableResponseMixin, CreateView):
    model = Ticket
    fields = 'name', 'description'
    success_url = reverse_lazy('ticket-list')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
            response = super().form_valid(form)
        else:
            response = super().form_valid(form)
            # Add ticket.id (UUID) to session['ticket'] -> list of strings
            id = [str(self.object.pk)]  # Convert UUID to [str]
            ticket = self.request.session.get('ticket', []) + id
            self.request.session['ticket'] = ticket
        return response
