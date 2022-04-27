# """
# File in which we have the middleware for Django for Authenticating API requests
# """
# import json
# import jwt
# import logging
# from django.http import HttpResponse
# from django.utils.deprecation import MiddlewareMixin

# # Initialize logger
# logger = logging.getLogger(__name__)

# # Get JWT secret key
# SECRET_KEY = "jhbkjvhgchgfxfdzszesxgvhj"


# def create_response(request_id, code, message):
#     try:
#         req = str(request_id)
#         data = {"data": message, "code": int(code), "request_id": req}
#         return data
#     except Exception as creation_error:
#         logger.error(f'create_response:{creation_error}')


# class CustomMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         jwt_token = request.headers.get('authorization', None)
#         logger.info(f"request received for endpoint {str(request.path)}")

#         if jwt_token:
#             try:
#                 payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=['HS256'])
#                 userid = payload['user_id']
#                 company_id = payload['company_id'] if 'company_id' in payload else None
#                 logger.info(f"Request received from user - {userid}, company - {company_id}")
#                 return None
#             except jwt.ExpiredSignatureError:
#                 response = create_response("", 4001, {"message": "Authentication token has expired"})
#                 logger.info(f"Response {response}")
#                 return HttpResponse(json.dumps(response), status=401)
#             except (jwt.DecodeError, jwt.InvalidTokenError):
#                 response = create_response("", 4001, {"message": "Authorization has failed, Please send valid token."})
#                 logger.info(f"Response {response}")
#                 return HttpResponse(json.dumps(response), status=401)
#         else:
#             response = create_response(
#                 "", 4001, {"message": "Authorization not found, Please send valid token in headers"}
#             )
#             logger.info(f"Response {response}")
#             return HttpResponse(json.dumps(response), status=401)



# import json
# import jwt
# import logging
# from django.http import HttpResponse
# from django.utils.deprecation import MiddlewareMixin
# from django.utils.deprecation import MiddlewareMixin

# class MySimpleMiddleware(MiddlewareMixin):

#     def __init__(self, get_response):
#         self.get_response = get_response

#     def process_request(self, request):
#             print("something")
#             try:
#                 request.session['my_message'] = "boss"
#             except:
#                 request.session['my_message']  = "ok"



import re
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth import logout

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')
        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)

        if path == reverse('accounts:logout').lstrip('/'):
            logout(request)

        if request.user.is_authenticated() and url_is_exempt:
            return redirect(settings.LOGIN_REDIRECT_URL)
        elif request.user.is_authenticated() or url_is_exempt:
            return None
        else:
            return redirect(settings.LOGIN_URL)