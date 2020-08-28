import json
from urllib import request


def fill_code(code):
    return '0' * (6 - len(code)) + code


def get_north_bond_top(date):
    url = 'https://www.hkex.com.hk/chi/csm/DailyStat/data_tab_daily_%sc.js' % date
    req = request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Host': 'www.hkex.com.hk'
    })
    response = request.urlopen(req)
    content = response.read()
    body = content.decode('utf-8')
    data = json.loads(body.replace('\\', '').split('=')[1])
    sse = data[0]['content'][1]['table']['tr']
    sze = data[2]['content'][1]['table']['tr']
    return [fill_code(item['td'][0][1]) for item in sse + sze]
