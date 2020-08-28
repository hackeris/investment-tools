import xlrd
import datetime

from urllib import request


def get_index_weights(code):
    now_time_stamp = int(datetime.datetime.now().timestamp())
    url = 'http://www.csindex.com.cn/uploads/file/autofile/closeweight/' \
          '%scloseweight.xls?t=%d' % (code, now_time_stamp)
    response = request.urlopen(url)
    xls_data = response.read()
    book = xlrd.open_workbook(file_contents=xls_data)
    sheets = list(book.sheets())
    for i, sheet in enumerate(sheets):
        for row in range(1, sheet.nrows):
            code_cell = sheet.cell(row, 4)
            weight_cell = sheet.cell(row, 8)
            yield code_cell.value, float(weight_cell.value) / 100


def get_index_list(code):
    now_time_stamp = int(datetime.datetime.now().timestamp())
    url = 'http://www.csindex.com.cn/uploads/file/autofile/cons/%scons.xls?t=%d' % (code, now_time_stamp)
    response = request.urlopen(url)
    xls_data = response.read()
    book = xlrd.open_workbook(file_contents=xls_data)
    sheets = list(book.sheets())
    for i, sheet in enumerate(sheets):
        for row in range(1, sheet.nrows):
            code_cell = sheet.cell(row, 4)
            yield code_cell.value
