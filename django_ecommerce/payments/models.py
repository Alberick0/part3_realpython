from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from main.models import Badge


class User(AbstractBaseUser):
    name = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=50)

    # password field defined in base class
    last_4_digits = models.CharField(max_length=4, blank=True, null=True)
    stripe_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rank = models.CharField(max_length=50, default='Padwan')
    badge = models.ManyToManyField(Badge)

    USERNAME_FIELD = 'email'  # describes a unique field as an unique Identifier

    bigCoID = models.CharField(max_length=50, unique=True)

    @classmethod
    def get_by_id(cls, uid):
        """
        This method is stateless, when calling it there's no need to create a
        User object
        :param uid:
        """
        return User.objects.get(pk=uid)

    @classmethod
    def create(cls, name, email, password, last_4_digits, stripe_id):
        new_user = cls(name=name, email=email, last_4_digits=last_4_digits,
                       stripe_id=stripe_id)
        new_user.set_password(password)
        new_user.bigCoID = '{}{}{}'.format(
            new_user.name[:2], new_user.rank[:1],
            datetime.now().strftime('%Y%m%d%H%M%S%f'),
        )
        new_user.save()

        return new_user

    def __str__(self):
        return self.email


class UnPaidUsers(models.Model):
    email = models.CharField(max_length=100, unique=True)

    # with 'auto_now' there's no need to import datetime
    last_notification = models.DateTimeField(auto_now=True)
