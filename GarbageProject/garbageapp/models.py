from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Registration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    contactnumber = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

class Complain(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    register = models.ForeignKey(Registration, on_delete=models.CASCADE, null=True, blank=True)
    complain = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    locality = models.CharField(max_length=100, null=True, blank=True)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    note = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    completed = models.CharField(max_length=100, null=True, blank=True)
    work = models.CharField(max_length=100, null=True, blank=True)
    remaining = models.CharField(max_length=100, null=True, blank=True)
    photo = models.FileField(null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.register.user.username

class Bin(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, blank=True)
    complain = models.ForeignKey(Complain, on_delete=models.CASCADE, null=True, blank=True)
    idname = models.CharField(max_length=100, null=True, blank=True)
    area = models.CharField(max_length=100, null=True, blank=True)
    locality = models.CharField(max_length=100, null=True, blank=True)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    loadtype = models.CharField(max_length=100, null=True, blank=True)
    period = models.CharField(max_length=100, null=True, blank=True)
    bus = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    creationdate = models.DateTimeField(auto_now_add=True)

class Trackinghistory(models.Model):
    complain = models.ForeignKey(Complain, on_delete=models.CASCADE, null=True, blank=True)
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)

