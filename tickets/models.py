import uuid
from django.urls import reverse
from django.db import models
from django.conf import settings


class Ticket(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(
        max_length=255,
        verbose_name='Condition or drug to add')
    description = models.TextField(max_length=1023, blank=True)
    admin_notes = models.TextField(max_length=1023, blank=True)
    actioned = models.BooleanField(default=False)
    for_review = models.BooleanField(
        default=False,
        verbose_name='Mark for review')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='ticket_created_by')
    last_edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='ticket_edited_by')

    def get_absolute_url(self):
        return reverse('ticket-update', kwargs={'pk': self.id})

    def __str__(self):
        return self.name
