import uuid
from django.db import models
from django.conf import settings
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from reactions.models import Interaction


class Review(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    interaction = models.ForeignKey(
        Interaction,
        related_name='interaction',
        on_delete=models.CASCADE)
    comment = MarkdownxField()
    date_created = models.DateTimeField(auto_now_add=True)
    actioned = models.BooleanField(default=False)

    def comment_markdown(self):
        return markdownify(self.comment)

    def get_absolute_url(self):
        return reverse("review_detail", kwargs={"pk": self.id})

    def __str__(self):
        return f'Peer reivew of interaction: \
            {self.interaction.name} on {self.date_created}'


class ReviewSession(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    interaction_reviews = models.ManyToManyField(
        Review,
        related_name='interaction_reviews',
        blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    open = models.BooleanField(default=False)
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Host for the peer review session',
        null=True,
        blank=True,
        related_name='host')
    user_list = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name='Users present during the peer review session',
        blank=True,
        related_name='user_list')

    def user_list_string(self):
        return ' ,'.join(user.username for user in self.user_list.all())

    def get_absolute_url(self):
        return reverse("session_detail", kwargs={"pk": self.id})

    def __str__(self):
        return f'Review session started {self.date_created}'
