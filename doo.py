import xlrd
import xlsxwriter
import json


class Excel:

    def __init__(self, file_name, mode='r'):
        if mode == 'r':
            self.workbook = xlrd.open_workbook(file_name)
        elif mode == 'w':
            self.workbook = xlsxwriter.Workbook(file_name)
        else:
            raise Exception(
                'Error: init Excel class with error mode: %s' % mode)

    def get_sheets_name(self):
        names = []
        for name in self.workbook.sheet_names():
            names.append(name)
        return names

    def read_sheet(self, sheet_name):
        '''
        sheet_name: Excel 中标签页名称
        return：[[],[]……]
        '''
        sheet = self.workbook.sheet_by_name(sheet_name)
        nrows = sheet.nrows
        data = []
        for i in range(nrows):
            data.append(sheet.row_values(i))
        return data

    def read_sheets(self):
        sheets = self.get_sheets_name()
        if 'INDEX' not in sheets:
            raise Exception('No INDEX sheet')

        data = {}
        for sheet in sheets:
            d = self.read_sheet(sheet)
            data[sheet] = d
        return data

    def close(self):
        self.workbook.close()


def index2json(data):
    index = {'Title': '', 'Description': '', 'Version': '',
             'BasePath': '', 'REQUEST': {}, 'RESPONSE': {}}
    flag = ''
    for d in data:
        if d[0] in index.keys():
            index[d[0]] = d[1]
        elif d[0] == '请求Headers':
            flag = 'REQUEST'
            continue
        elif d[0] == '响应Headers':
            flag = 'RESPONSE'
            continue

        if flag == 'REQUEST' and d[1]:
            index['REQUEST'][d[1]] = d[2]

        if flag == 'RESPONSE':
            if d[1]:
                index['RESPONSE'][d[1]] = d[2]
            else:
                break

    return index


def message(protocol, d, one, headers=False, num=0):
    if d[0].upper() == 'HEADERS':
        headers = True
    elif d[0].upper() == 'BODY':
        headers = False

    if d[1]:
        data = [v for v in d[6:6 + num]]
        field = {'name': d[1], 'cnname': d[2], 'type': d[3],
                 'must': d[4], 'remark': d[5], 'data': data}
        if headers:
            one[protocol]['HEADERS'][d[1]] = field
        else:
            one[protocol]['BODY'][d[1]] = field
    return one


def doc2json(data):
    doc = {}

    # key:sheet_name, value:sheet_data
    for key, value in data.items():
        group = []
        flag = 'NEW'
        headers = False
        num = 0
        # d: sheet_row,value: sheet_rows
        for d in value:
            if flag == 'NEW':
                one = {'名称': '', '描述': '', '接口地址': '', '方法': '', '权限': '',
                       'REQUEST': {'HEADERS': {}, 'BODY': {}},
                       'RESPONSE': {'HEADERS': {}, 'BODY': {}}}
                flag = 'N'
                headers = False

            if d[0] in one.keys():
                one[d[0]] = d[1]
            elif d[0] == '请求':
                flag = 'REQUEST'
                num = len([v for v in d[6:] if v])
                continue
            elif d[0] == '响应':
                flag = 'RESPONSE'
                one['status_code'] = [int(v) for v in d[6:6 + num]]
                continue
            elif d[0] == '测试数据备注':
                flag = 'NEW'
                one['remark'] = [v for v in d[6:6 + num]]

            if flag == 'REQUEST':
                one = message('REQUEST', d, one, headers, num)

            if flag == 'RESPONSE':
                one = message('RESPONSE', d, one, headers, num)

            if flag == 'NEW':
                group.append(one)

        doc[key] = group

    return doc


if __name__ == '__main__':
    e = Excel('doo.xlsx')
    data = e.read_sheets()

    index = index2json(data.pop('INDEX'))
    print('--- INDEX ---')
    print(json.dumps(index, ensure_ascii=False, indent=4))

    doc = doc2json(data)
    print('\n--- DOC ---')
    print(json.dumps(doc, ensure_ascii=False, indent=4))
