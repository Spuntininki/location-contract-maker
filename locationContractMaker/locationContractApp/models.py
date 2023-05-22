from email.policy import default
from unittest.util import _MAX_LENGTH

from django.db import models

# Create your models here.


class owner(models.Model):
    owner_full_name = models.CharField(max_length=45)
    owner_cpf = models.IntegerField()
    owner_rg = models.IntegerField()


class tenant(models.Model):
    tenant_full_name = models.CharField(max_length=45)
    tenant_cpf = models.IntegerField()
    tenant_rg = models.IntegerField()
    active = models.BooleanField(default=False)
    contract_start_date = models.DateField()
    contract_end_date = models.DateField()


class property(models.Model):
    property_adress = models.CharField(max_length=50)
    property_adress_number = models.CharField(max_length=4)
    property_adress_complement = models.CharField(max_length=10)
    property_adress_district = models.CharField(max_length=20)
    property_adress_city = models.CharField(max_length=20)
    property_tenant = models.ForeignKey(
        tenant, on_delete=models.SET_NULL, null=True
    )
    located = models.BooleanField(default=False)
