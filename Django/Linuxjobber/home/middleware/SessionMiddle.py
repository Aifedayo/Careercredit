from datetime import datetime

from decouple import config
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.deprecation import MiddlewareMixin

from django.conf import settings


class SessionMiddleWare(MiddlewareMixin):
    def process_request(self,request):
        if 'timeout' in request.path or 'login' in request.path or 'logout' in request.path:
            if "logout" in request.path:
                request.session['has_timeout']=False
            return

        if request.user.is_authenticated:
            if request.session.get('has_timeout',None) == True:
                return redirect('home:timeout')

            last_activity = request.session.get('last_activity',None)
            now = datetime.now()
            if last_activity:
                if (now -  datetime.strptime(last_activity,"%Y,%m,%d,%H,%M,%S")).total_seconds() > config("SESSION_TIMEOUT_IN_SECOND", 1800,cast=int):
                    request.session['from_timeout_next'] = request.path
                    request.session['has_timeout'] = True
                    request.session['last_activity'] = now.strftime("%Y,%m,%d,%H,%M,%S")
                    # Do logout / expire session
                    # and then...
                    return redirect('home:timeout')
            if not request.is_ajax():
                # don't set this for ajax requests or else your
                # expired session checks will keep the session from
                # expiring :)

                request.session['last_activity'] = now.strftime("%Y,%m,%d,%H,%M,%S")
                if not request.session.get("has_timeout", None):
                    request.session['has_timeout'] = False
