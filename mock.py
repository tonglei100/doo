from apistar import Route, Include, http
import copy
import sys
from time import sleep
from doo.cap import CapApp
from doo.excel import Excel


type_map = {'int': 'int',
            'string': 'str',
            'float': 'float',
            'bool': 'bool'
            }


def func():
    return f"""def {key.lower()}(request: http.Request, params: http.QueryParams{pkts}):
            '''
            描述： {desc}
            '''

            return response('{key}', request, params{pkws})"""


def home():
    '''
    描述: Doo 首页
    '''

    return {'Name': 'Doo',
            'Author': 'tonglei',
            'Github': 'https://github.com/tonglei100/doo'}


def check_body(body_doc, body_real, **kwarg):
    for k in body_doc:
        if k.startswith('{') and k.endswith('}'):
            if body_doc[k] != kwarg.get(k[1:-1]):
                return False
        else:
            if body_doc[k] != body_real.get(k):
                return False
    return True


def response(api, request: http.Request, params, **kwarg):
    params = dict(params)
    headers = dict(request.headers)
    if doc[api]['方法'] == 'POST':
        body = eval(request.body.decode('utf-8'))
    else:
        body = {}

    headers_doc = doc[api]['REQUEST']['Headers']
    for k in headers_doc:
        if headers_doc[k] != headers.get(k.lower()):
            return http.JSONResponse(f'Headers is not matching\ndoc \
            {k}:{headers_doc[k]}\nreal {k}:{headers.get(k)}', status_code=404)

    req_data_doc = doc[api]['REQUEST']['Data']
    res_data_doc = doc[api]['RESPONSE']['Data']
    body = dict(body, **params)
    for i in range(len(req_data_doc)):
        result = check_body(req_data_doc[i], body, **kwarg)
        if result:
            if doc[api].get('delay'):
                sleep(doc[api]['delay'][i])
            return http.JSONResponse(res_data_doc[i], status_code=doc[api]['status_code'][i], headers=doc[api]['RESPONSE']['Headers'])

    return http.JSONResponse('No body data matching', status_code=404)

if len(sys.argv) >1:
    excel_file = sys.argv[1]
else:
    excel_file = 'example.xlsx'

e = Excel(excel_file)
doc = e.get_data()

for key in doc:
    desc = doc[key]['描述']
    pkts = ''
    pkws = ''
    body = doc[key]['REQUEST']['Body']
    for k in body:
        if k.startswith('{') and k.endswith('}'):
            pkts += ', ' + k[1:-1] + ': ' + type_map[body[k]['type'].lower()]
            pkws += ', ' + k[1:-1] + '=' + k[1:-1]
        exec(func())

routes = [Route('/', method='GET', handler=home)]

for key in doc:
    url = doc[key]['接口地址']
    method = doc[key]['方法']
    handler = getattr(sys.modules[__name__], key.lower())

    routes.append(Route(url, method=method, handler=handler))

app = CapApp(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)
