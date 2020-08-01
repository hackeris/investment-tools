import json
from urllib import request


def fill_code(code):
    return '0' * (6 - len(code)) + code


def get_north_bond_top(date):
    url = 'https://www.hkex.com.hk/chi/csm/DailyStat/data_tab_daily_%sc.js' % date
    response = request.urlopen(url)
    body = response.read().decode('utf-8')
    data = json.loads(body.split('=')[1])
    sse = data[0]['content'][1]['table']['tr']
    sze = data[2]['content'][1]['table']['tr']
    return [fill_code(item['td'][0][1]) for item in sse + sze]
