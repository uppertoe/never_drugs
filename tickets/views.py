from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now, timedelta

from core.utilities import JsonableResponseMixin
from .models import Ticket

# Create your views here.
class TicketListView(LoginRequiredMixin, ListView):
    context_object_name = 'ticket_list'
    template_name = 'tickets/ticket_list.html'

    def get_queryset(self):
        '''Show superusers all (non-actioned) Tickets, and logged-in users their own Tickets'''
        if self.request.user.is_superuser:
            return Ticket.objects.filter(actioned=False)
        else:
            return Ticket.objects.filter(created_by=self.request.user)

class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    context_object_name = 'ticket'
    template_name = 'tickets/ticket_detail.html'

class TicketCreateView(JsonableResponseMixin, CreateView):
    model = Ticket
    fields = 'name', 'description'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.created_by = self.request.user
        return super().form_valid(form)

class TicketUpdateView(UpdateView):
    model = Ticket
    fields = 'name', 'description'


    def get_context_data(self, **kwargs):
        '''
        Ticket delete button available when existing_ticket == True
        Allow if ticket created within 1 hour of datetime.now()
        '''
        context = super().get_context_data(**kwargs)
        print(self.object.date_created)
        print(now() - timedelta(hours=1))
        if self.object.date_created > now() - timedelta(hours=1):
            context['existing_ticket'] = True
        return context

class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = reverse_lazy('ticket-list')