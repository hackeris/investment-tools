import json
from urllib import request


def get_qfii_holding_volumes(report_date):
    url_template = 'http://datainterface3.eastmoney.com/EM_DataCenter_V3/api/JJSJTJ/GetJJSJTJ?' \
                   'tkn=eastmoney&ReportDate=' + report_date + '&code=&type=2&zjc=0&sortField=Count&sortDirec=1&' \
                                                               'pageNum=%d&pageSize=50&cfg=jjsjtj'
    url = url_template % 1
    response = request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))['Data'][0]
    total_page = data['TotalPage']
    for line in data['Data']:
        fields = line.split('|')
        yield fields[0], int(fields[7]), float(fields[9]) / 100

    for page in range(2, total_page):
        url = url_template % page
        response = request.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))['Data'][0]
        for line in data['Data']:
            fields = line.split('|')
            yield fields[0], int(fields[7]), float(fields[9]) / 100
