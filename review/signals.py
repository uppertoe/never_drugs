from django.dispatch import receiver
from django.db.models.signals import post_save

from reactions.models import Interaction
from .models import Review


@receiver(post_save, sender=Interaction)
def create_associated_review(sender, instance, **kwargs):
    review = Review.objects.filter(interaction=instance)
    if not review:
        review = Review.objects.create(interaction=instance)
        review.save()
        print(f'Review created for {instance}')
