import xlrd
import xlsxwriter
import json
import copy
import yaml
import sys
from pathlib import Path

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
             'BasePath': '', 'Request_Headers': {}, 'Response_Headers': {}}
    flag = ''
    for d in data:
        if d[0] in index.keys():
            index[d[0]] = d[1]
        elif d[0].replace(' ','').lower() == 'requestheaders':
            flag = 'REQUEST'
            continue
        elif d[0].replace(' ','').lower() == 'responseheaders':
            flag = 'RESPONSE'
            continue

        if flag == 'REQUEST' and d[1]:
            index['Request_Headers'][d[1]] = d[2]

        if flag == 'RESPONSE':
            if d[1]:
                index['Response_Headers'][d[1]] = d[2]
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
        field = [d[3], d[4], d[2], d[5]]
        if headers:
            one[protocol]['Headers'][d[1]] = data[0]
        else:
            one[protocol]['Body'][d[1]] = field
            for i in range(num):
                if not one.get('DATA'+str(i+1)):
                    one['DATA'+str(i+1)] = {'REQUEST':{}, 'RESPONSE': {}}
                t = data[i]

                if d[3] == 'string':
                    t = str(data[i])
                elif d[3] == 'int':
                    t = int(data[i])
                elif d[3] == 'float':
                    t = float(data[i])
                elif d[3] == 'json':
                    try:
                        t = json.loads(data[i])
                    except:
                       raise Exception(f'Excel\'s json error,key {d[1]}:\n{data[i]}')

                if d[1] == 'Body':
                    one['DATA'+str(i+1)][protocol] = dict(one['DATA'+str(i+1)][protocol], **t)
                else:
                    one['DATA'+str(i+1)][protocol][d[1]] = t

    return one


def doc2json(data, index):
    doc = {}
    cn = {'名称': 'Name', '描述': 'Desc', '接口': 'Path', '方法': 'Method', '权限': 'Auth'}
    # key:sheet_name, value:sheet_data
    for key, value in data.items():
        flag = 'NEW'
        headers = False
        num = 0
        # d: sheet_row,value: sheet_rows
        for d in value:

            if flag == 'NEW':
                one = {'Name': '', 'Desc': '', 'Path': '', 'Method': '', 'Auth': '', 'GROUP': key,
                       'REQUEST': {'Headers': copy.deepcopy(index['Request_Headers']), 'Body': {}},
                       'RESPONSE': {'Headers': copy.deepcopy(index['Response_Headers']), 'Body': {}}}
                flag = 'N'
                headers = False

            if d[0] in cn.keys():
                k = cn[d[0]]
                one[k] = d[1]
            elif d[0].upper() in ('请求', 'REQUEST'):
                flag = 'REQUEST'
                num = len([v for v in d[6:] if v])
                if one['Method'] == 'GET':
                    one['REQUEST']['Headers'].pop('Content-Type')
                for i in range(num):
                    if not one.get('DATA'+str(i+1)):
                        one['DATA'+str(i+1)] = {'REQUEST':{}, 'RESPONSE': {}}
                continue
            elif d[0].upper() in ('响应', 'RESPONSE'):
                flag = 'RESPONSE'
                for i in range(num):
                    one['DATA'+str(i+1)]['status_code'] = int(d[6+i]) if d[6+i] else 200
                continue
            elif d[0].upper() in ('响应延时', 'DELAY'):
                for i in range(num):
                    one['DATA'+str(i+1)]['delay'] = float(d[6+i]) if d[6+i] else 0

            elif d[0].upper() in ('测试数据备注', 'REMARK'):
                flag = 'NEW'
                for i in range(num):
                    one['DATA'+str(i+1)]['remark'] = d[6+i] if d[6+i] else ''

            if flag in ('REQUEST', 'RESPONSE'):
                one = message(flag, d, one, headers, num)

            if flag == 'NEW':
                one['Name'] = one['Name'].upper()
                doc[one['Name']] = one


    return doc


class Yaml():
    def __init__(self, path, mode='r'):
        self.files = []
        if  path.is_dir():
            self.files = list(path.glob('*.yml'))
        elif path.exists():
            if path.suffix == '.yml':
                self.files.append(path)

    def get_data(self):
        index = {'REQUEST_Headers': {}, 'RESPONSE_Headers': {}}
        doc = {}
        for yaml_file in self.files:
            f = open(yaml_file, encoding='utf-8')
            cont =f.read()
            y = yaml.load_all(cont)
            for api in y:
                if api.get('Name'):
                    doc[api['Name'].upper()] = api
                elif api.get('Title'):
                    index = api

        for name,api in doc.items():
            if not api['REQUEST'].get('Headers'):
                api['REQUEST']['Headers'] = {}
            api['REQUEST']['Headers'] = dict(index['REQUEST_Headers'], **api['REQUEST']['Headers'])
            if api['Method'] == 'GET':
                api['REQUEST']['Headers'].pop('Content-Type')

        return doc


def star_sort(doc):
    for api in doc:
        star = {}
        for k in api:
            if 'DATA' in k:
                for field,value in api[k]['REQUEST'].items():
                    if  isinstance(value, str) and value == '*':
                        if not api[k].get('star'):
                            api[k]['star'] = 1
                        else:
                            api[k]['star'] += 1
                if api[k].get('star'):
                    star[k] = api[k]['star']
        star = sorted(star.items(), key=lambda d:d[1],reverse=False)
        for k in dict(star):
            v = api[k]
            api.pop(k)
            api[k] = v

    return doc


def get_doc():

    extra_files = []
    doc = {}
    if len(sys.argv) >1:
        api_file = sys.argv[1]
        path = Path(api_file)

        if path.exists():
            if path.suffix == '.xlsx':
                    e = Excel(api_file)
                    doc = e.get_data()
                    extra_files.append(path)
            else :
                y = Yaml(path)
                doc = y.get_data()
                extra_files = y.files
        else:
            print(f'--- The api file/folder:{api_file} is not exists ---')
            sys.exit(-1)
    else:
        if Path('example.yml').exists():
            y = Yaml(Path('example.yml'))
            doc = y.get_data()
            extra_files.append(Path('example.yml'))
        elif Path('example.xlsx').exists():
            e = Excel(Path('example.xlsx'))
            doc = e.get_data()
            extra_files.append(Path('example.xlsx'))
        else:
            print('--- Please input .xlsx or .yml file ---')
            sys.exit(-1)

    return star_sort(doc), extra_files


if __name__ == '__main__':

    doc = get_doc()

    print('\n--- DOC ---')
    print(json.dumps(doc, ensure_ascii=False, indent=4))
