from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
import rbac.apps as rbac_settings


class RbacMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.bjm = 'Benjamin142857'
        print('MD001 - process_request')

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('MD001 - process_view [start]')
        print(view_func, view_args, view_kwargs)
        print('MD001 - process_view [end]')

    # def process_exception(self, request, exception):
    #     print('MD001-error : {}'.format(exception))
    #     return HttpResponse('MD001-error : {}'.format(exception))

    # def process_template_response(self, request, response):
    #     print('MD001 - process_template_response')
    #     print(response)
    #     if rbac_settings.DEBUG:
    #         pass
    #     print(response)
    #     return response

    def process_response(self, request, response):
        print('MD001 - process_response')
        return response