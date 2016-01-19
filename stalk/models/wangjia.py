from django.db import models
from lolly import Lolly


class Navigation(Lolly):
    pin = models.CharField(unique=True, max_length=20)
    allPin = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=50, null=True)
    link = models.URLField(null=True)
    province_id = models.PositiveSmallIntegerField(default=0)
    launch_time = models.CharField(max_length=10, null=True)
    icon_url = models.URLField(null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'wangjia_navigation'

    def get_uk_code(self):
        return str(self.id)+'_'+self.pin


class Archive(Lolly):
    navigation = models.OneToOneField('Navigation', to_field='id', db_column='id', primary_key=True)
    name = models.CharField(max_length=50, null=True)
    link = models.URLField(null=True)
    launch_time = models.CharField(max_length=10, null=True)
    logo_url = models.URLField(null=True)
    location = models.CharField(max_length=20, null=True)
    introduction = models.TextField(null=True)
    company_name = models.CharField(max_length=50, null=True)
    artificial_person = models.CharField(max_length=50, null=True)
    company_type = models.CharField(max_length=50, null=True)
    shareholder_stucture = models.CharField(max_length=500, null=True)
    registered_capital = models.CharField(max_length=50, null=True)
    contributed_capital = models.CharField(max_length=50, null=True)
    registered_address = models.CharField(max_length=100, null=True)
    opening_date = models.CharField(max_length=20, null=True)
    approved_date = models.CharField(max_length=20, null=True)
    registration_authority = models.CharField(max_length=50, null=True)
    business_licence = models.CharField(max_length=50, null=True)
    institutional_framework = models.CharField(max_length=50, null=True)
    tax_registration_num = models.CharField(max_length=50, null=True)
    domain_name = models.CharField(max_length=150, null=True)
    domain_date = models.CharField(max_length=20, null=True)
    domain_company_type = models.CharField(max_length=50, null=True)
    domain_company_name = models.CharField(max_length=50, null=True)
    icp = models.CharField(max_length=50, null=True)
    company_person_avatar_url = models.TextField(null=True)
    company_person = models.TextField(null=True)
    management_fee = models.TextField(null=True)
    prepaid_fee = models.TextField(null=True)
    cash_withdrawal_fee = models.TextField(null=True)
    vip_fee = models.TextField(null=True)
    transfer_fee = models.TextField(null=True)
    mode_of_payment = models.CharField(max_length=50, null=True)
    contact_address = models.CharField(max_length=100, null=True)
    phone_400 = models.CharField(max_length=20, null=True)
    phone = models.CharField(max_length=20, null=True)
    fax = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    is_automatic_bid = models.CharField(max_length=50, null=True)
    is_equitable_assignment = models.CharField(max_length=50, null=True)
    trust_fund = models.CharField(max_length=100, null=True)
    tender_security = models.CharField(max_length=100, null=True)
    security_mode = models.CharField(max_length=100, null=True)
    guarantee_institution = models.CharField(max_length=300, null=True)
    business_type = models.CharField(max_length=100, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'wangjia_archive'

    def get_uk_code(self):
        return str(self.navigation.id)+'_'+self.navigation.pin


class Problem(Lolly):
    name = models.CharField(unique=True,max_length=50)
    pin = models.CharField(max_length=20)
    problem_time = models.CharField(max_length=10, null=True)
    launch_time = models.CharField(max_length=10, null=True)
    registered_capital = models.CharField(max_length=50, null=True)
    province_id = models.PositiveSmallIntegerField(default=0)
    accounted_revenue = models.CharField(max_length=50, null=True)
    involved_passenger = models.CharField(max_length=50, null=True)
    event_category = models.CharField(max_length=20, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'wangjia_problem'


class Rating(Lolly):
    name = models.CharField(max_length=50)
    timestamp = models.CharField(max_length=10)
    exponent = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    launch_time = models.CharField(max_length=10, null=True)
    location = models.CharField(max_length=20, null=True)
    deal = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    popularity = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    profit = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    revenue = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    lever = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    brand = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    dispersity = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    mobility = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    transparency = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'wangjia_rating'
        unique_together = ('name', 'timestamp')


class Data(Lolly):
    name = models.CharField(max_length=50)
    timestamp = models.CharField(max_length=10)
    volume = models.CharField(max_length=50, null=True)
    investment_passenger = models.CharField(max_length=50, null=True)
    loan_passenger = models.CharField(max_length=50, null=True)
    average_interest_rate = models.CharField(max_length=50, null=True)
    average_loan_period = models.CharField(max_length=50, null=True)
    loan_bid = models.CharField(max_length=50, null=True)
    registered_capital = models.CharField(max_length=50, null=True)
    time_for_full_bid = models.CharField(max_length=50, null=True)
    accounted_revenue = models.CharField(max_length=50, null=True)
    capital_inflow_in_30_days = models.CharField(max_length=50, null=True)
    volumn_weighted_time = models.CharField(max_length=50, null=True)
    accounted_revenue_in_60_days = models.CharField(max_length=50, null=True)
    proportion_of_top_10_tuhao_accounted_revenue = models.CharField(max_length=50, null=True)
    average_investment_amount = models.CharField(max_length=50, null=True)
    proportion_of_top_10_borrower_accounted_revenue = models.CharField(max_length=50, null=True)
    average_loan_amount = models.CharField(max_length=50, null=True)
    capital_lever = models.CharField(max_length=50, null=True)
    operation_time = models.CharField(max_length=50, null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'wangjia_data'
        unique_together = ('name', 'timestamp')


class Exposure(Lolly):
    thread = models.CharField(unique=True, max_length=20)
    source = models.URLField(null=True)
    title = models.CharField(max_length=500, null=True)
    created = models.CharField(max_length=20, null=True)
    name = models.CharField(max_length=60, null=True)
    link = models.URLField(null=True)
    reason = models.TextField(null=True)
    content = models.TextField(null=True)
    raw_content = models.TextField(null=True)
    image_url = models.TextField(null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'wangjia_exposure'

    #TODO: (zacky, 2015.JUN.3rd) NEED TO ABSTRACT HERE.
    def get_uk_code(self):
        return 'thread_'+str(self.id)


class NewsCategory(Lolly):
    name = models.CharField(unique=True, max_length=20)

    class Meta:
        app_label = 'stalk'
        db_table = 'wangjia_news_category'


class News(Lolly):
    thread = models.CharField(max_length=10)
    category_id = models.PositiveSmallIntegerField(default=0)
    source = models.URLField(null=True)
    title = models.CharField(max_length=500, null=True)
    created = models.CharField(max_length=20, null=True)
    author = models.CharField(max_length=50, null=True)
    summary = models.TextField(null=True)
    content = models.TextField(null=True)
    raw_content = models.TextField(null=True)
    image_url = models.TextField(null=True)

    class Meta:
        app_label = 'stalk'
        db_table = 'wangjia_news'
        unique_together = ('thread', 'category_id')

    def get_uk_code(self):
        return 'thread_'+str(self.id)
