from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    # other fields...

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Sensor(models.Model):
    name = models.CharField(max_length=30)
    key = models.CharField(max_length=30)
    max = models.IntegerField()
    last_synchro = models.DateTimeField(default=timezone.now)
    premium_date = models.DateTimeField(default=timezone.now)
    is_premium = models.BooleanField()
    def __str__(self):
        return u'%s' % (self.name)

class Unit(models.Model):
    name = models.CharField(max_length=20)
    unit = models.CharField(max_length=10)
    key = models.CharField(max_length=20)
    min = models.FloatField()
    max = models.FloatField()
    color = models.CharField(max_length=10)

    def __str__(self):
        return u'%s' % (self.name)

class measurement(models.Model):
    sensor = models.ForeignKey(Sensor)
    date = models.DateTimeField(default=timezone.now)
    value = models.FloatField()
    unit = models.ForeignKey(Unit)

class user_sensor(models.Model):
    user = models.ForeignKey(User)
    sensor = models.ForeignKey(Sensor)
    name = models.CharField(max_length=30)

