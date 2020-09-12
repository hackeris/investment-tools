import sys
from datetime import datetime
from urllib import request
from crawler.csi import get_index_list


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


def get_trade_volume_of(symbols):
    url = 'http://hq.sinajs.cn/list=' + ','.join(symbols)
    response = request.urlopen(url)
    lines = response.read().decode('gbk').split('\n')
    items = []
    for symbol, line in zip(symbols, lines[:len(symbols)]):
        fields = line.split(',')
        volume = int(fields[8])
        items.append((symbol[2:], volume))
    return items


def _main():
    out_dir = sys.argv[1]
    all_a = list(get_index_list('000985'))
    symbols = ['sh' + code if code[0] == '6' else 'sz' + code
               for code in all_a]

    volumes = []
    for chunk in chunks(symbols, 100):
        items = get_trade_volume_of(chunk)
        volumes.extend(items)

    today = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open('%s/info_r_%s.csv' % (out_dir, today), 'w') as f:
        for item in volumes:
            f.write('%s,%d\n' % item)


if __name__ == '__main__':
    retries = 5
    while retries > 0:
        try:
            _main()
            break
        except Exception as e:
            retries -= 1
