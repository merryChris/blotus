# -*- coding: utf-8 -*-
from django.db import models
from lolly import Lolly

class LoanInfo(Lolly):
    loan_id = models.CharField(max_length=10,unique=True)
    title = models.CharField(max_length=50,null=True)
    status = models.CharField(max_length=15,null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'renrendai_loaninfo'

class Borrower(Lolly):
    loan_id = models.CharField(max_length=10,unique=True)
    user_id = models.CharField(max_length=50,null=True)
    user_nickname = models.CharField(max_length=50,null=True)
    age = models.IntegerField()
    education = models.CharField(max_length=50,null=True)
    marriage = models.CharField(max_length=50,null=True)
    #companyIndustry = models.CharField(max_length=50,null=True)
    #companyScale = models.CharField(max_length=50,null=True)
    #companyPosition = models.CharField(max_length=50,null=True)
    city = models.CharField(max_length=50,null=True)
    length_of_service = models.CharField(max_length=50,null=True)
    income_scale = models.CharField(max_length=50,null=True)
    #houseProperty = models.CharField(max_length=50,null=True)
    #houseLoan = models.CharField(max_length=50,null=True)
    #carProperty = models.CharField(max_length=50,null=True)
    #carLoan = models.CharField(max_length=50,null=True)

    credit_level = models.CharField(max_length=50,null=True)
    loan_application_num = models.IntegerField()
    success_application_num = models.IntegerField()
    payoff_num = models.IntegerField()
    credit_line = models.FloatField()
    total_loan_amount = models.FloatField()
    total_left_to_pay = models.FloatField()
    overdue_amount = models.FloatField()
    overdue_times = models.IntegerField()
    critical_overdue_times = models.IntegerField()

    class Meta:
        app_label = 'stalk'
        db_table = 'renrendai_borrower'

class Product(Lolly):
    loan_id = models.CharField(max_length=10,unique=True)
    product_name = models.CharField(max_length=50,null=True)
    amount = models.FloatField()
    income_ratio = models.FloatField()
    pay_period = models.IntegerField()
    guarantee_method = models.CharField(max_length=50,null=True)
    pre_pay_ratio = models.FloatField()
    pay_method = models.CharField(max_length=50,null=True)
    #payPerMonth = models.FloatField()
    #leftToPay = models.FloatField()
    #leftPayPeriod = models.IntegerField()
    #nextPayDate = models.CharField(max_length=50,null=True)

    loan_detail = models.TextField()

    #borrower = models.ForeignKey(borrower,default='')

    class Meta:
        app_label = 'stalk'
        db_table = 'renrendai_product'

class InvestRecord(Lolly):
    loan_id = models.CharField(max_length=10,null=True)
    user_id = models.CharField(max_length=10,null=True)
    amount = models.FloatField()
    lend_time = models.DateTimeField(default='')

    class Meta:
        app_label = 'stalk'
        db_table = 'renrendai_investrecord'
        unique_together = ('loan_id','user_id','lend_time')