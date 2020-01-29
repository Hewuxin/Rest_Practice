from django.db import models


class User(models.Model):
    u_name = models.CharField(max_length=128, unique=True)
    u_password = models.CharField(max_length=128)

    class Meta:
        db_table = 'user'


class Address(models.Model):
    a_address = models.CharField(max_length=256)
    a_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'address'
