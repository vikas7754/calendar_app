from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.views import View
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from django.conf import settings


# Google Calendar credentials
# CLIENT_ID = 'your-client-id'
# CLIENT_SECRET = 'your-client-secret'
REDIRECT_URI = 'http://127.0.0.1:8000/rest/v1/calendar/redirect/'
CLIENT_SECRET_FILE = settings.FIXTURES_ROOT + 'client_secrets.json'


def index(req):
    return HttpResponse("<h1>Hello World!</h1>")


class GoogleCalendarInitView(View):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=REDIRECT_URI
        )
        auth_url, _ = flow.authorization_url(prompt='consent')
        return redirect(auth_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        code = request.GET.get('code')
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRET_FILE,
            scopes=['https://www.googleapis.com/auth/calendar.readonly'],
            redirect_uri=REDIRECT_URI
        )
        flow.fetch_token(code=code)
        credentials = flow.credentials

        service = build('calendar', 'v3', credentials=credentials)
        events_result = service.events().list(calendarId='primary', maxResults=10).execute()
        events = events_result.get('items', [])

        return JsonResponse(events, safe=False)
