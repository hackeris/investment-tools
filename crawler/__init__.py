import datetime

from crawler.hkex import get_north_bond_top
from crawler.xueqiu import get_k_line_of, values_of, parse_timestamp, get_finance_indicator, get_k_line_of_stock


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


def total_revenue_q_from_indicators(indicators):
    """
    indicators must be get_finance_indicator(xxx, indicator_type='all')
    """
    rg_l4q = []
    for i in range(len(indicators['list']) - 1):
        cur, prev = indicators['list'][i], indicators['list'][i + 1]
        if '一季报' in cur['report_name']:
            rg_l4q.append(dict(
                report_name=cur['report_name'],
                total_revenue=cur['total_revenue'][0],
                growth_l4q=cur['total_revenue'][1]
            ))
        else:
            prev_rpt_revenue_q = cur['total_revenue'][0] / (1 + cur['total_revenue'][1]) \
                                 - prev['total_revenue'][0] / (1 + prev['total_revenue'][1])
            curr_rpt_revenue_q = cur['total_revenue'][0] - prev['total_revenue'][0]
            rg_l4q.append(dict(
                report_name=cur['report_name'],
                total_revenue=curr_rpt_revenue_q,
                growth_l4q=curr_rpt_revenue_q / prev_rpt_revenue_q - 1
            ))
    return rg_l4q


def get_total_revenue_q_of_stocks(stocks):
    items = dict()
    for code in stocks:
        print('Getting total_revenue_q of stock: %s' % (code,))
        items[code] = total_revenue_q_from_indicators(get_finance_indicator(code, 'all'))
    return items


def get_k_line_of_stocks(stocks):
    lines = {}
    for code in stocks:
        print('Getting market data of stock: %s' % code)
        lines[code] = get_k_line_of_stock(code)
    return lines
