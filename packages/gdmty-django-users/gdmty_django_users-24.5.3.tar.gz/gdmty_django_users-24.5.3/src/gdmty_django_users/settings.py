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

import os
from django.conf import settings
import logging
from . import __title__

log = logging.getLogger(__title__)

ENABLE_RECAPTCHA = getattr(settings, 'ENABLE_RECAPTCHA', False)
