from django.shortcuts import redirect
from .cron import *

class SessionMiddleware:
    def __init__(self, get_response):
        start_timer()
        self.get_response = get_response

    def __call__(self, request):
        try:
            session_id = request.COOKIES.get('session_id')
            try:
                session_object = Session.objects.get(session_id=session_id)
                if session_object.expires_at > timezone.now():
                    response = self.get_response(request)
                    return response
                else:
                    session_object.delete()
            except Session.DoesNotExist:
                pass
        except KeyError:
            pass
        if request.path.startswith('/login/') or request.path.startswith('/registration/'):
            return self.get_response(request)
        else:
            return redirect('login')