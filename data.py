import datetime

from source.hkex import get_north_bond_top
from source.xueqiu import get_k_line_of, values_of, parse_timestamp, get_finance_indicator, get_k_line_of_stock


def get_prev_trading_days():
    secx = get_k_line_of('SH000001')
    return [datetime.datetime.strftime(parse_timestamp(it), '%Y%m%d')
            for it in values_of(secx, 'timestamp')]


def get_hk_north_stocks_of_days(dates):
    stocks = set()
    for date in dates:
        print('Getting HK North stocks of day: %s' % date)
        codes = get_north_bond_top(date)
        for c in codes: stocks.add(c)
    return list(stocks)


def get_indicators_of_stocks(stocks, indicator_type='all'):
    indicators = dict()
    for code in stocks:
        print('Getting %s indicators of stock: %s' % (indicator_type, code))
        indicators[code] = get_finance_indicator(code, indicator_type)
    return indicators


def get_k_line_of_stocks(stocks):
    lines = {}
    for code in stocks:
        print('Getting market data of stock: %s' % code)
        lines[code] = get_k_line_of_stock(code)
    return lines
