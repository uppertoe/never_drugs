import uuid
from django.dispatch import receiver
from allauth.account.signals import user_logged_in

from .models import Ticket

# Register in the 'ready' method of AppConfig in apps.py

@receiver(user_logged_in)
def attach_user_to_tickets(sender, request, user, **kwargs):
    if request.session.get('ticket'):
        ticket_list = request.session.get('ticket')
        for ticket in ticket_list:
            try:
                instance = Ticket.objects.get(id=uuid.UUID(ticket))
                if not instance.created_by:
                    instance.created_by = user
                    instance.save()
            except:
                print(f'Error attaching {user} to ticket {ticket} on login')