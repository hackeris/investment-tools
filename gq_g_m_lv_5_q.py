import operator
from typing import List

import numpy as np

from data import get_indicators_of_stocks, get_k_line_of_stocks
from source.csi import get_index_list
from source.xueqiu import values_of


def momentum(prices: List[float], start, end):
    start = len(prices) - abs(start) if start < 0 else start
    end = (len(prices) - abs(end)) if end < 0 else end
    start_price = prices[0] if start < 0 else prices[start]
    end_price = prices[0] if end < 0 else prices[end]
    return end_price / start_price - 1


def _main():
    print('Getting stock list of SH000300')
    csi300 = list(get_index_list('000300'))

    market_lines = get_k_line_of_stocks(csi300)
    prices = dict([(code, values_of(data, 'close')) for code, data in market_lines.items()])
    daily_yields = dict([(code, values_of(data, 'percent')) for code, data in market_lines.items()])
    momentum_6m_adj = dict([(code, momentum(prices.get(code), -22 * 6, -22)) for code in csi300])
    volatility_90d = dict([(code, np.std(daily_yields.get(code)[-90:]) * np.sqrt(250) / 100) for code in csi300])

    indicators_q = get_indicators_of_stocks(csi300)
    indicators_q4 = get_indicators_of_stocks(csi300, 'Q4')

    revenue_growth_1 = dict([(code, indicators_q.get(code)['list'][0]['total_revenue'][1]) for code in csi300])
    revenue_growth_2 = dict([(code, indicators_q.get(code)['list'][1]['total_revenue'][1]) for code in csi300])
    revenue_growth_3 = dict([(code, indicators_q.get(code)['list'][2]['total_revenue'][1]) for code in csi300])

    roe_1 = dict([(code, indicators_q4.get(code)['list'][0]['avg_roe'][0] / 100) for code in csi300])
    roe_2 = dict([(code, indicators_q4.get(code)['list'][1]['avg_roe'][0] / 100) for code in csi300])
    roe_3 = dict([(code, indicators_q4.get(code)['list'][2]['avg_roe'][0] / 100) for code in csi300])

    def growth_quality_selector(code):
        rg1 = revenue_growth_1.get(code)
        rg2 = revenue_growth_2.get(code)
        rg3 = revenue_growth_3.get(code)
        q1 = roe_1.get(code)
        q2 = roe_2.get(code)
        q3 = roe_3.get(code)
        return rg1 > 0.15 and rg2 > 0.15 and rg3 > 0.15 and q1 > 0.15 and q2 > 0.15 and q3 > 0.15

    growth_quality_selected = [code for code in csi300 if growth_quality_selector(code)]

    revenue_growth_sorted = sorted([
        (code, revenue_growth_1.get(code))
        for code in growth_quality_selected
    ], key=operator.itemgetter(1), reverse=True)
    revenue_growth_selected = [code for code, g in revenue_growth_sorted[:20]]

    momentum_sorted = sorted([
        (code, momentum_6m_adj.get(code))
        for code in revenue_growth_selected
    ], key=operator.itemgetter(1), reverse=True)
    momentum_selected = [code for code, m in momentum_sorted[:10]]

    volatility_sorted = sorted([
        (code, volatility_90d.get(code))
        for code in momentum_selected
    ], key=operator.itemgetter(1))
    volatility_selected = [code for code, v in volatility_sorted[:5]]

    print('-------------- STOCKS --------------')
    for code in volatility_selected:
        print(code)


if __name__ == '__main__':
    _main()
