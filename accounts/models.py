from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class Meta:
        permissions = (("access_peer_review", "Can access the peer review module"),)
        verbose_name = "User"
