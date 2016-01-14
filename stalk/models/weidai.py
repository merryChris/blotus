from django.db import models
from lolly import Lolly


class Tender(Lolly):
    pin = models.CharField(unique=True, max_length=10)
    location = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=50, null=True)
    interest_rate = models.CharField(max_length=20, null=True)
    time_limit = models.CharField(max_length=20, null=True)
    launch_date = models.CharField(max_length=20, null=True)
    volume = models.CharField(max_length=20, null=True)
    transfer_amount = models.CharField(max_length=20, null=True)
    progress = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=20, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'weidai_tender'


class Bid(Lolly):
    tender = models.OneToOneField('Tender', to_field='id', db_column='id', primary_key=True)
    title = models.CharField(max_length=50, null=True)
    feature = models.CharField(max_length=50, null=True)
    volume = models.CharField(max_length=50, null=True)
    annual_profit = models.CharField(max_length=20)
    time_limit = models.CharField(max_length=20, null=True)
    interest_time = models.CharField(max_length=20, null=True)
    mode_of_payment = models.CharField(max_length=50, null=True)
    launch_time = models.CharField(max_length=10, null=True)
    progress = models.CharField(max_length=20, null=True)
    source_strore = models.CharField(max_length=20, null=True)
    has_security_guarantee = models.PositiveSmallIntegerField(default=0)
    user = models.CharField(max_length=20, null=True)
    gender = models.CharField(max_length=20, null=True)
    marital_status = models.CharField(max_length=20, null=True)
    hometown = models.CharField(max_length=50, null=True)
    payoffed = models.CharField(max_length=20, null=True)
    pending = models.CharField(max_length=20, null=True)
    overdue = models.CharField(max_length=20, null=True)
    vehicle_brand = models.CharField(max_length=20, null=True)
    vehicle_number = models.CharField(max_length=20, null=True)
    vehicle_kilometers = models.CharField(max_length=20, null=True)
    vehicle_price = models.CharField(max_length=20, null=True)
    mortgage_value = models.CharField(max_length=20, null=True)
    verification_time = models.CharField(max_length=20, null=True)
    verification_explanation = models.CharField(max_length=20, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'weidai_bid'


class Bidder(Lolly):
    pin = models.CharField(max_length=10)
    mobile = models.CharField(max_length=20, null=True)
    amount = models.CharField(max_length=20, null=True)
    time = models.CharField(max_length=20, null=True)
    source = models.CharField(max_length=20, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'weidai_bidder'
