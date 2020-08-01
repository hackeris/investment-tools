import json
import time
import zlib
import datetime
import http.cookiejar

from urllib import request


def _symbol_of(code):
    return ('SH' + code) if (code[0] == '6') else ('SZ' + code)


def build_opener():
    jar = http.cookiejar.CookieJar()
    handler = request.HTTPCookieProcessor(jar)
    opener = request.build_opener(handler)
    return opener


def get_cookie(opener):
    url = 'https://xueqiu.com'
    req = request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Host': 'xueqiu.com',
        'Accept-Encoding': 'gzip',
    })
    opener.open(req)


_opener = build_opener()
get_cookie(_opener)


def xueqiu_http_get(url, headers=None):
    req = request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
        'Accept-Encoding': 'gzip',
        **(headers or {})
    })
    result = _opener.open(req)
    if result.info().get('Content-Encoding') == 'gzip':
        buf = zlib.decompress(result.read(), 16 + zlib.MAX_WBITS)
        resp = buf.decode('utf-8')
    else:
        resp = result.read().decode('utf-8')
    data = json.loads(resp)
    return data['data']


def get_k_line_of_stock(code):
    return get_k_line_of(_symbol_of(code))


def get_k_line_of(symbol):
    tomorrow = int((datetime.datetime.now() + datetime.timedelta(days=1)).timestamp() * 1000)
    url = ('https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=%s&begin=%d&period=day'
           '&type=before&count=-284&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance') % (
              symbol, tomorrow)
    return xueqiu_http_get(url)


def get_finance_indicator(code, indicator_type='all'):
    """
    :param code:
    :param indicator_type: Can be 'all', 'Q4', 'Q3', 'Q2', 'Q1'
    :return:
    """
    symbol = _symbol_of(code)
    url = 'https://stock.xueqiu.com/v5/stock/finance/cn/indicator.json?' \
          'symbol=%s&type=%s&is_detail=true&count=5&timestamp=' % (symbol, indicator_type)
    return xueqiu_http_get(url, headers={
        'Origin': 'https://xueqiu.com',
        'Referer': 'https://xueqiu.com/snowman/S/%s/detail' % symbol
    })


def parse_timestamp(ts):
    if isinstance(ts, str):
        ts = int(ts)
    ts = ts / 1000
    return datetime.datetime.fromtimestamp(ts)


def values_of(data, column):
    col = data['column'].index(column)
    return [item[col] for item in data['item']]
