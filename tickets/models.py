import uuid
from django.db import models
from django.conf import settings

# Create your models here.
class Ticket(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid64,
        editable=False)
    condition = models.CharField(max_length=255)
    drugs = models.CharField(max_length=255, blank=True)
    description = models.TextField(max_length=1023, blank=True)
    admin_notes = models.TextField(max_length=1023, blank=True)
    actioned = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name = 'ticket_edited_by',
    )

    def __str__(self):
        return self.condition

