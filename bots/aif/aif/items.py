# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from bots.base.items import BaseItem
from stalk.models import aif


class JibenItem(BaseItem):
    django_model = aif.Basic
    update_fields_list = ['plat_id', 'date', 'turnover_amount', 'trade_amount', 'borrower_amount',           \
                          'investor_amount', 'loan_amount_per_capita', 'avg_loan_per_trade',                 \
                          'invest_amount_per_capita', 'avg_invest_per_trade', 'loan_balance',                \
                          'max_borrower_ratio', 'topten_borrowers_ratio', 'avg_full_time',                   \
                          'accum_default_rate', 'product_overdue_rate', 'three_month_overdue_rate',          \
                          'overdue_loan_amount', 'compensatory_amount', 'loan_overdue_rate',                 \
                          'bad_debt_rate', 'customer_complaints', 'customer_complaints_solve',               \
                          'interest_rate', 'avg_borrow_period', 'topten_investor_ratio',                     \
                          'financial_leverage', 'repaid_amount']
    unique_key = ('plat_id', 'date')

class MeiriItem(BaseItem):
    django_model = aif.Daily
    update_fields_list = ['plat_id', 'date', 'daily_turnover', 'daily_trade_cnt', 'daily_invest_cnt',        \
                          'thityday_income', 'service_time']
    unique_key = ('plat_id', 'date')
