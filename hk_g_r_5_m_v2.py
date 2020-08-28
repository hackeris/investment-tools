import operator

from crawler import get_prev_trading_days, get_hk_north_stocks_of_days, get_indicators_of_stocks, get_k_line_of_stocks, \
    get_total_revenue_q_of_stocks
from crawler.xueqiu import values_of


def _main():
    dates = get_prev_trading_days()
    hk_north_stocks = get_hk_north_stocks_of_days(dates[-5:])
    total_revenue_q = get_total_revenue_q_of_stocks(hk_north_stocks)
    market_lines = get_k_line_of_stocks(hk_north_stocks)
    prices = dict([(code, values_of(data, 'close'))
                   for code, data in market_lines.items()])

    last_prices = [
        (code, prices.get(code)[-1])
        for code in hk_north_stocks
    ]
    price_selected = [code for code, price in last_prices if 5 <= price <= 200]

    revenue_growth_l4q_sorted = sorted([
        (code, total_revenue_q[code][0]['growth_l4q'])
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

    print('-------------- STOCKS --------------')
    for code in selected:
        print(code)


if __name__ == '__main__':
    _main()
