# middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class RestrictAnonymousMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path_info.lstrip('/')
        if 'private_files' in path and not request.user.is_authenticated:
            return redirect(reverse('login') + '?next=' + request.path)
        return response
