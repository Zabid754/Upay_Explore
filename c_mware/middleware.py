import datetime
import os
from django.conf import settings

class VisitorLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        path = request.path

        log_entry = f"[{time_now}] IP: {ip_address} | Path: {path} | Browser: {user_agent}\n"

        # 3. Save to a file in your project root
        log_path = os.path.join(settings.BASE_DIR, "visitor_log.txt")
        with open(log_path, "a") as f:
            f.write(log_entry)

        # 4. Continue to the next step (the View)
        response = self.get_response(request)
        return response