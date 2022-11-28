# signals.py registered in the 'ready' method of AppConfig in apps.py
import uuid
from django.dispatch import receiver
from allauth.account.signals import user_logged_in

from .models import Ticket


@receiver(user_logged_in)
def attach_user_to_tickets(sender, request, user, **kwargs):
    tickets = request.session.get('ticket')
    if tickets:
        for ticket in tickets:
            try:
                instance = Ticket.objects.get(id=uuid.UUID(ticket))
                if not instance.created_by:
                    instance.created_by = user
                    instance.save()
            except Ticket.DoesNotExist:
                print(f'Error attaching {user} to ticket {ticket} on login')
        del request.session['ticket']
        return print(f'{user} login; tickets {tickets} attached')
    return print(f'{user} login; no tickets to attach')
