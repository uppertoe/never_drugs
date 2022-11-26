from django.dispatch import receiver
from django.db.models.signals import post_save

from reactions.models import Condition
from .models import Review


@receiver(post_save, sender=Condition)
def create_associated_review(sender, instance, **kwargs):
    review = Review.objects.filter(condition=instance)
    if not review:
        review = Review.objects.create(condition=instance)
        review.save()
        print(f'Review created for {instance}')
