import xlrd
import xlsxwriter
import json
import copy


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

    def get_data(self):
        data = self.read_sheets()
        self.index = index2json(data.pop('INDEX'))
        self.doc = doc2json(data, copy.deepcopy(self.index))
        return self.doc

    def close(self):
        self.workbook.close()


def index2json(data):
    index = {'Title': '', 'Description': '', 'Version': '',
             'BasePath': '', 'REQUEST_Headers': {}, 'RESPONSE_Headers': {}}
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
            index['REQUEST_Headers'][d[1]] = d[2]

        if flag == 'RESPONSE':
            if d[1]:
                index['RESPONSE_Headers'][d[1]] = d[2]
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
            one[protocol]['Headers'][d[1]] = field['data'][0]
        else:
            one[protocol]['Body'][d[1]] = field
    return one


def doc2json(data, index):
    doc = {}

    # key:sheet_name, value:sheet_data
    for key, value in data.items():
        flag = 'NEW'
        headers = False
        num = 0
        # d: sheet_row,value: sheet_rows
        for d in value:
            if flag == 'NEW':
                one = {'名称': '', '描述': '', '接口地址': '', '方法': '', '权限': '', 'GROUP': key,
                       'REQUEST': {'Headers': copy.deepcopy(index['REQUEST_Headers']), 'Body': {}},
                       'RESPONSE': {'Headers': copy.deepcopy(index['RESPONSE_Headers']), 'Body': {}}}
                flag = 'N'
                headers = False

            if d[0] in one.keys():
                one[d[0]] = d[1]
            elif d[0] == '请求':
                flag = 'REQUEST'
                num = len([v for v in d[6:] if v])
                if one['方法'] == 'GET':
                    one['REQUEST']['Headers'].pop('Content-Type')
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
                one['名称'] = one['名称'].upper()
                one['REQUEST']['Data'] = body_data(one['REQUEST']['Body'])
                one['RESPONSE']['Data'] = body_data(one['RESPONSE']['Body'])
                doc[one['名称']] = one


    return doc


def body_data(body):
    data = []
    num = len(body[list(body.keys())[0]]['data'])
    for i in range(num):
        d = {}
        for key in body:
            if body[key]['type'] == 'string':
                d[key] = str(body[key]['data'][i])
            elif body[key]['type'] == 'int':
                d[key] = int(body[key]['data'][i])
            elif body[key]['type'] == 'float':
                d[key] = float(body[key]['data'][i])
            elif body[key]['type'] == 'json':
                try:
                    d[key] = json.loads(body[key]['data'][i])
                except:
                   raise Exception('Excel 中的 json 格式错误,key %s:\n%s' %(key, str(body[key]['data'][i])))
                if body[key]['name'] == 'Body':
                    d = dict(d, **d.pop(key))
        data.append(d)
    return data


if __name__ == '__main__':
    e = Excel('EMOS.xlsx')
    data = e.get_data()

    print('--- INDEX ---')
    print(json.dumps(e.index, ensure_ascii=False, indent=4))

    print('\n--- DOC ---')
    print(json.dumps(e.doc, ensure_ascii=False, indent=4))
