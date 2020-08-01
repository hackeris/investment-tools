import datetime
import operator

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


def get_indicators_of_stocks(stocks):
    indicators = dict()
    for code in stocks:
        print('Getting indicators of stock: %s' % code)
        indicators[code] = get_finance_indicator(code, 'all')
    return indicators


def get_k_line_of_stocks(stocks):
    lines = {}
    for code in stocks:
        print('Getting market data of stock: %s' % code)
        lines[code] = get_k_line_of_stock(code)
    return lines


def _main():
    dates = get_prev_trading_days()
    hk_north_stocks = get_hk_north_stocks_of_days(dates[-5:])
    indicators = get_indicators_of_stocks(hk_north_stocks)
    market_lines = get_k_line_of_stocks(hk_north_stocks)
    prices = dict([(code, values_of(data, 'close'))
                   for code, data in market_lines.items()])

    last_prices = [
        (code, prices.get(code)[-1])
        for code in hk_north_stocks
    ]
    price_selected = [code for code, price in last_prices if 5 <= price <= 200]

    revenue_growth_l4q_sorted = sorted([
        (code, indicators[code]['list'][0]['total_revenue'][1])
        for code in price_selected
    ], key=operator.itemgetter(1), reverse=True)
    growth_selected = [
        code for code, g in revenue_growth_l4q_sorted[:10]
    ]

    reversal_1m_sorted = sorted([
        (code, prices.get(code)[-1] / prices.get(code)[-22])
        for code in growth_selected
    ], key=operator.itemgetter(1))
    selected = [code for code, r in reversal_1m_sorted[:5]]

    for code in selected:
        print(code)


if __name__ == '__main__':
    _main()
