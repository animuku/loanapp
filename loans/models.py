from django.db import models

class Address(models.Model):
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200,blank=True,null=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zip = models.IntegerField(blank=True)


class Owners(models.Model):
    name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    dob = models.DateTimeField()
    phone = models.IntegerField(blank=True)
    ssn = models.IntegerField(blank=True)
    percent_own = models.FloatField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Business(models.Model):
    name = models.CharField(max_length=200)
    annual_revenue = models.FloatField()
    avg_bank_balance = models.FloatField()
    avg_credit_card_volume = models.FloatField()
    tax_id = models.IntegerField(blank=True)
    phone = models.IntegerField(blank=True)
    naics = models.IntegerField(blank=True)
    has_been_profitable = models.BooleanField()
    bankrupted = models.BooleanField()
    inception_date = models.DateField()
    owners = models.ManyToManyField(Owners)
    has_been_updated = models.BooleanField()
    address = models.ForeignKey(Address, on_delete=models.CASCADE)


class Requests(models.Model):
    loan_amount = models.FloatField(blank=True)
    credit_history = models.IntegerField(blank=True)
    entity_type = models.CharField(max_length=200)
    filter_id = models.IntegerField(blank=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)


