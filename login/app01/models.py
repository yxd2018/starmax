# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(verbose_name="用户",max_length=64)
    password = models.CharField(verbose_name="密码",max_length=64)