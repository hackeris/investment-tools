import operator

from data import get_indicators_of_stocks, get_k_line_of_stocks
from source.eastmoney import get_qfii_holding_volumes
from source.xueqiu import values_of


def _main():
    report_date = input('QFII Report Day(See from http://data.eastmoney.com/zlsj/2020-03-31-2-2.html), like 2020-03-31: ')

    print('Getting QFII holding of stocks')
    qfii_volumes = list(get_qfii_holding_volumes(report_date))

    qfii_universe = [code for code, vol, ratio in qfii_volumes]
    market_lines = get_k_line_of_stocks(qfii_universe)
    prices = dict([(code, values_of(data, 'close'))
                   for code, data in market_lines.items()])
    last_prices = dict([(code, prices.get(code)[-1]) for code in qfii_universe])

    qfii_volumes = [(code, vol, vol * last_prices.get(code), ratio) for code, vol, ratio in qfii_volumes]

    qfii_sorted = sorted(qfii_volumes, key=operator.itemgetter(2), reverse=True)
    qfii_selected = [code for code, vol, mv, ratio in qfii_sorted[:20]]

    indicators_q = get_indicators_of_stocks(qfii_selected)
    indicators_q4 = get_indicators_of_stocks(qfii_selected, 'Q4')

    roe = dict([(code, indicators_q4.get(code)['list'][0]['avg_roe'][0] / 100)
                for code in qfii_selected])
    revenue_growth = dict([(code, indicators_q.get(code)['list'][0]['total_revenue'][1])
                           for code in qfii_selected])

    roe_sorted = sorted([
        (code, roe.get(code))
        for code in qfii_selected
    ], key=operator.itemgetter(1), reverse=True)
    roe_selected = [code for code, m in roe_sorted[:10]]

    revenue_growth_sorted = sorted([
        (code, revenue_growth.get(code))
        for code in roe_selected
    ], key=operator.itemgetter(1), reverse=True)
    revenue_growth_selected = [code for code, g in revenue_growth_sorted[:5]]

    print('-------------- STOCKS --------------')
    for code in revenue_growth_selected:
        print(code)


if __name__ == '__main__':
    _main()
