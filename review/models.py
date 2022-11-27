import uuid
from django.db import models
from django.conf import settings
from django.urls import reverse
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

from reactions.models import Condition


class Review(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    condition = models.ForeignKey(
        Condition,
        related_name='Condition',
        on_delete=models.CASCADE)
    comment = MarkdownxField(blank=True, null=True, default='')
    update = MarkdownxField(blank=True, null=True, default='')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    actioned = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_created']

    def comment_markdown(self):
        return markdownify(self.comment) if self.comment else ''

    def update_markdown(self):
        return markdownify(self.update) if self.update else ''

    def get_absolute_url(self):
        return reverse("review_detail", kwargs={"pk": self.id})

    def __str__(self):
        name = self.condition.name.capitalize()
        author = self.condition.created_by.username.capitalize()
        return f'\'{name}\' by {author}'


class ReviewSession(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    reviews = models.ManyToManyField(
        Review,
        related_name='reviews',
        verbose_name='Articles for peer review',
        blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    last_ajax = models.DateTimeField(blank=True, null=True)
    open = models.BooleanField(default=False)
    host = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Chairperson for the meeting',
        null=True,
        blank=True,
        related_name='host')
    user_list = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name='Users present during the peer review session',
        blank=True,
        related_name='user_list')

    class Meta:
        ordering = ['-date_created']

    def user_list_string(self):
        users = self.user_list.all()
        return ', '.join(user.username.capitalize() for user in users)

    def get_ajax_url(self):
        return reverse("ajax_review_detail") + f"?id={self.id}"

    def get_absolute_url(self):
        return reverse("session_detail", kwargs={"pk": self.id})

    def __str__(self):
        return f'Review session started {self.date_created}'
