from django.db import models
from lolly import Lolly


class Loan(Lolly):
    plat_id = models.CharField(max_length=20)
    plat_name = models.CharField(max_length=50, null=True)
    bid_id = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=20, null=True)
    title = models.CharField(max_length=50, null=True)
    amount = models.CharField(max_length=20, null=True)
    process = models.CharField(max_length=20, null=True)
    interest_rate = models.CharField(max_length=20, null=True)
    borrow_period = models.CharField(max_length=20, null=True)
    borrow_unit = models.CharField(max_length=20, null=True)
    reward = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=20, null=True)
    repay_type = models.CharField(max_length=20, null=True)
    username = models.CharField(max_length=20, null=True)
    user_id = models.CharField(max_length=20, null=True)
    user_avatar_url = models.TextField(null=True)
    province = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=20, null=True)
    borrow_detail = models.TextField(null=True)
    url = models.TextField(null=True)
    success_time = models.CharField(max_length=20, null=True)
    publish_time = models.CharField(max_length=20, null=True)
    invest_count = models.CharField(max_length=20, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'enterprise_loan'
        unique_together = ('plat_id', 'bid_id')


class Invest(Lolly):
    plat_id = models.CharField(max_length=20)
    plat_name = models.CharField(max_length=50, null=True)
    invest_id = models.CharField(max_length=50, null=True)
    bid_id = models.CharField(max_length=20, null=True)
    user_id = models.CharField(max_length=20, null=True)
    username = models.CharField(max_length=20, null=True)
    amount = models.CharField(max_length=20, null=True)
    valid_amount = models.CharField(max_length=20, null=True)
    add_date = models.CharField(max_length=20, null=True)
    status = models.CharField(max_length=20, null=True)
    type = models.CharField(max_length=20, null=True)
    url = models.TextField(null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'enterprise_invest'
        unique_together = ('plat_id', 'invest_id')


class Overdue(Lolly):
    plat_id = models.CharField(max_length=20)
    plat_name = models.CharField(max_length=50, null=True)
    user_id = models.CharField(max_length=20, null=True)
    username = models.CharField(max_length=20, null=True)
    idcard = models.CharField(max_length=20, null=True)
    overdue_count = models.CharField(max_length=20, null=True)
    overdue_total = models.CharField(max_length=20, null=True)
    overdue_principal = models.CharField(max_length=20, null=True)
    payment_total = models.CharField(max_length=20, null=True)
    payment_count = models.CharField(max_length=20, null=True)
    payment_period = models.CharField(max_length=20, null=True)
    repay_amount = models.CharField(max_length=20, null=True)
    wait_amount = models.CharField(max_length=20, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'enterprise_overdue'
        unique_together = ('plat_id', 'user_id')
