from apistar import Route, Include, http
import copy
import sys
from pathlib import Path
from time import sleep
from doo.cap import CapApp
from doo.data import Excel, Yaml, get_doc


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
    for k,v in body_doc.items():
        # 如果 Mock 数据的值是减号(-)，则真实请求中该字段应该不存在
        if v == '-':
            if body_real.get(k):
                return False
        # 如果是加号(+)，则真实请求中，该字段存在即可
        elif v == '+':
            if not body_real.get(k):
                return False
        # 如果是星号(*)，则真实请求中，该字段存在或不存在都可以
        elif v == '*':
            continue
        # 如果是星号(*)开头，则真实请求中，模糊匹配
        elif v.startswith('*'):
            if not isinstance(body_real.get(k), str):
                return False
            elif v[1:] not in body_real.get(k):
                return False
        # 如果是上尖号(^)开头，则真实请求中，开头匹配
        elif v.startswith('^'):
            if not isinstance(body_real.get(k), str):
                return False
            elif not body_real.get(k).startswith(v[1:]):
                return False
        # 如果是 Dollar($)开头，则真实请求中，末尾匹配
        elif v.startswith('^'):
            if not isinstance(body_real.get(k), str):
                return False
            elif not body_real.get(k).endswith(v[1:]):
                return False


        if isinstance(body_doc[k], str) and body_doc[k].startswith('\\'):
            body_doc[k] = body_doc[k][1:]
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
    if doc[api]['Method'] == 'POST':
        body = eval(request.body.decode('utf-8'))
    else:
        body = {}

    headers_doc = doc[api]['REQUEST']['Headers']
    for k in headers_doc:
        if headers_doc[k] != headers.get(k.lower()):
            return http.JSONResponse(f'Headers is not matching\ndoc \
            {k}:{headers_doc[k]}\nreal {k}:{headers.get(k)}', status_code=404)

    body = dict(body, **params)
    for data in doc[api]:
        if 'DATA' in data:
            result = check_body(doc[api][data]['REQUEST'], body, **kwarg)
            if result:
                if doc[api][data].get('delay'):
                    sleep(doc[api][data]['delay'])
                return http.JSONResponse(doc[api][data]['RESPONSE'], \
                status_code=doc[api][data].get('status_code', 200), headers=doc[api]['RESPONSE']['Headers'])

    return http.JSONResponse('No body data matching', status_code=404)

doc = get_doc()

for key in doc:
    desc = doc[key]['Desc']
    pkts = ''
    pkws = ''
    body = doc[key]['REQUEST']['Body']
    for k in body:
        if k.startswith('{') and k.endswith('}'):
            pkts += ', ' + k[1:-1] + ': ' + type_map[body[k][0].lower()]
            pkws += ', ' + k[1:-1] + '=' + k[1:-1]
    exec(func())

routes = [Route('/', method='GET', handler=home)]

for key in doc:
    url = doc[key]['Path']
    method = doc[key]['Method']
    handler = getattr(sys.modules[__name__], key.lower())

    routes.append(Route(url, method=method, handler=handler))

app = CapApp(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)
