#!-*- coding: utf-8 -*-
"""
Package that is an extension of Django's AbstractBaseUser for user management, using email as user.
This packages adds features such as group permissions and reCaptcha enterprise token verification.

This package is published as free software under the terms of the Apache License, Version 2.0. Is developed by
Dirección de Gobierno Digital of the Secretaría de Innovación y Gobierno Abierto of Municipality of Monterrey.

Authors: ['César Benjamín García Martínez <mathereall@gmail.com>', 'Miguel Angel Hernández Cortés
<miguelhdezc12@gmail.com>', 'César Guillermo Vázquez Álvarez <cdgva@outlook.com>']
Email: gobiernodigital@monterrey.gob.mx
GitHub: https://github.com/gobiernodigitalmonterrey/gdmty-django-users
Package: gdmty_django_users
PyPi: https://pypi.org/project/gdmty-django-users/
License: AGPL-3.0
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as OriginalGroup, Permission
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from .managers import CustomUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

username_validator = UnicodeUsernameValidator()


class User(AbstractUser):
    email = models.EmailField(unique=True)
    safe_delete = models.BooleanField(default=False)
    username = models.CharField(
        _("username"),
        max_length=150,
        primary_key=True,
        help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email_verificado = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    groups = models.ManyToManyField(
        OriginalGroup,
        verbose_name=_('groups'),
        blank=True,
        related_name='user_set',  # TODO: Add a related_name here
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='user_set',  # TODO: Add a related_name here
        related_query_name='user',
    )

    @property
    def id(self):
        return self.pk

    def __str__(self):
        return str(self.username or self.email)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        super(User, self).save(*args, **kwargs)

    @staticmethod
    @receiver(pre_delete, sender='gdmty_django_users.User')
    def safe_delete_user(sender, instance, **kwargs):
        instance.safe_delete = True
        instance.save()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class Group(OriginalGroup):
    class Meta:
        proxy = True
        verbose_name = "Group"
        verbose_name_plural = "Groups"
