from apistar import App
from apistar.http import Response
from apistar.server.wsgi import RESPONSE_STATUS_TEXT, WSGIStartResponse


def cap(o, s):
    c = [x.capitalize() for x in o.split(s)]
    return s.join(c)


class CapApp(App):
    '''
    由于 apistar 把 headers 的字段都改为了小写，故写此类
    继承 App，重构 Response.headers，把字段改为首字母大写
    '''
    def __init__(self,
                 routes,
                 template_dir=None,
                 static_dir=None,
                 packages=None,
                 schema_url='/schema/',
                 docs_url='/docs/',
                 static_url='/static/',
                 components=None,
                 event_hooks=None):

        super().__init__(routes,
                         template_dir=None,
                         static_dir=None,
                         packages=None,
                         schema_url='/schema/',
                         docs_url='/docs/',
                         static_url='/static/',
                         components=None,
                         event_hooks=None)

    def finalize_wsgi(self, response: Response, start_response: WSGIStartResponse):
        if self.debug and response.exc_info is not None:
            exc_info = response.exc_info
            raise exc_info[0].with_traceback(exc_info[1], exc_info[2])

        response.headers = [(cap(x[0], '-'), x[1]) for x in response.headers]
        start_response(
            RESPONSE_STATUS_TEXT[response.status_code],
            list(response.headers),
            response.exc_info
        )
        return [response.content]
