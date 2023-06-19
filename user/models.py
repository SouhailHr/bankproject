from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, IntegerField, ImageField, EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    #: First and last name do not cover name patterns around the globe
    full_name = CharField(_("Name"), blank=True, max_length=255)
    email = EmailField(unique=True)
    password = CharField(max_length=255)
    profile_picture = ImageField(upload_to='images/profile_pictures', null=True, blank=True)
    address = CharField(max_length=255, null=True, blank=True)
    phone_number = IntegerField(null=True, blank=True)

    # Add unique related_name arguments
    groups = None  # Set to None to avoid clashes
    user_permissions = None  # Set to None to avoid clashes

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
