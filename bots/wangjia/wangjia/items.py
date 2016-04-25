# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem, ProvinceItem
from stalk.models import wangjia

class DaohangItem(BaseItem):
    django_model = wangjia.Navigation
    update_fields_list = ['allPin', 'name', 'link', 'province_id', 'launch_time', 'icon_url']
    unique_key = ('pin',)

class DanganItem(BaseItem):
    django_model = wangjia.Archive
    update_fields_list = ['link', 'launch_time', 'location', 'logo_url', 'introduction', 'company_name',     \
                          'artificial_person', 'company_type', 'shareholder_stucture', 'registered_capital', \
                          'contributed_capital', 'registered_address', 'opening_date', 'approved_date',      \
                          'registration_authority', 'business_licence', 'institutional_framework',           \
                          'tax_registration_num', 'domain_name', 'domain_date', 'domain_company_type',       \
                          'domain_company_name', 'icp', 'company_person_avatar_url', 'company_person',       \
                          'management_fee', 'prepaid_fee', 'cash_withdrawal_fee', 'vip_fee', 'transfer_fee', \
                          'mode_of_payment', 'contact_address', 'phone_400', 'phone', 'fax', 'email',        \
                          'is_automatic_bid', 'is_equitable_assignment', 'trust_fund', 'tender_security',    \
                          'security_mode', 'guarantee_institution', 'business_type']
    related_field = 'archive'

class WentiItem(BaseItem):
    django_model = wangjia.Problem
    update_fields_list = ['pin', 'problem_time', 'launch_time', 'registered_capital', 'province_id',         \
                          'accounted_revenue', 'involved_passenger', 'event_category']
    unique_key = ('name',)

class PingjiItem(BaseItem):
    django_model = wangjia.Rating
    update_fields_list = ['name', 'timestamp', 'exponent', 'launch_time', 'location', 'deal', 'popularity',  \
                          'profit', 'revenue', 'lever', 'brand', 'dispersity','mobility','transparency']
    unique_key = ('name', 'timestamp')

class ShujuItem(BaseItem):
    django_model = wangjia.Data
    #  0 成交量
    #  1 投资人数
    #  2 借款人数
    #  3 平均利率
    #  4 平均借款期限
    #  5 借款标数
    #  6 注册资金
    #  7 满标用时
    #  8 累计待还金额
    #  9 近30日资金净流入
    # 10 时间加权成交量
    # 11 未来60日待还
    # 12 前十大土豪待收金额占比
    # 13 人均投资金额
    # 14 前十大借款人待还金额占比
    # 15 人均借款金额
    # 16 资金杠杆
    # 17 运营时间
    update_fields_list = ['name', 'timestamp', 'volume', 'investment_passenger', 'loan_passenger',           \
                          'average_interest_rate', 'average_loan_period', 'loan_bid', 'registered_capital',  \
                          'time_for_full_bid', 'accounted_revenue', 'capital_inflow_in_30_days',             \
                          'volumn_weighted_time', 'accounted_revenue_in_60_days',                            \
                          'proportion_of_top_10_tuhao_accounted_revenue', 'average_investment_amount',       \
                          'proportion_of_top_10_borrower_accounted_revenue', 'average_loan_amount',          \
                          'capital_lever', 'operation_time']
    unique_key = ('name', 'timestamp')

class BaoguangItem(BaseItem):
    django_model = wangjia.Exposure
    update_fields_list = ['source', 'title', 'created', 'name', 'link', 'reason', 'content', 'raw_content',  \
                          'image_url']
    unique_key = ('thread',)

class XinwenItem(BaseItem):
    django_model = wangjia.News
    update_field_list = ['thread', 'category_id', 'source', 'title', 'created', 'author', 'summary',         \
                         'content', 'raw_content', 'image_url']
    unique_key = ('thread', 'category_id')

class TedianItem(BaseItem):
    django_model = wangjia.Feature
    update_field_list = ['name',  'status', 'company_tag', 'illustration', 'recommendation', 'withdraw_num', \
                         'withdraw_day', 'guard_num', 'guard_day', 'service_num', 'service_status',          \
                         'experience_num', 'experience_status', 'impression']
    related_field = 'feature'
