from datetime import datetime

from decouple import config
from django.shortcuts import redirect


class SessionExpiredMiddleware(object):
    def process_request(self,request):
        if request.user.is_authenticated:
            last_activity = request.session['last_activity']
            now = datetime.now()

            if request.session['has_timeout'] or (now - last_activity).minutes > 10: #config("SESSION_TIMEOUT_IN_MINUTES",20,cast=int):
                request.session['has_timeout'] = True
                # Do logout / expire session
                # and then...
                return redirect("home:timeout")

            if not request.is_ajax():
                # don't set this for ajax requests or else your
                # expired session checks will keep the session from
                # expiring :)
                request.session['last_activity'] = now
                request.session['has_timeout'] = False