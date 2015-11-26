from django.http import QueryDict
 
class HttpPostTunnelingMiddleware(object):
    def process_request(self, request):
        if QueryDict(request.body).has_key('methodoverride'):
            http_method = QueryDict(request.body)['methodoverride']
            if http_method.lower() == 'put':
                request.method = 'PUT'
                request.META['REQUEST_METHOD'] = 'PUT'
                request.PUT = QueryDict(request.body)
            if http_method.lower() == 'delete':
                request.method = 'DELETE'
                request.META['REQUEST_METHOD'] = 'DELETE'
                request.DELETE = QueryDict(request.body)
        return None
