from django.shortcuts import render

# Create your views here.
import os
import datetime
from django.http import JsonResponse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError
from datetime import datetime, timedelta
from center.models import Center
from rest_framework.exceptions import NotFound

# Path to your service account key JSON file
# SERVICE_ACCOUNT_FILE = 'd4medicals/d4medicals\d4medicals-6ce951d3e1f7.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Get the current directory
current_directory = os.path.dirname(__file__)

# Move one directory up
parent_directory = os.path.abspath(os.path.join(current_directory, '..'))

# Specify the file name located one directory above
SERVICE_ACCOUNT_FILE = os.path.join(parent_directory, 'd4medicals-6ce951d3e1f7.json')

class GoogleCalendarCreateEventAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Adjust based on your authentication requirements
    def post(self, request):
        
        if not request.data.get('eventName'):
            return JsonResponse({'status': 'error', 'message': "Event name is required."}, status=500)
        if not request.data.get('eventDescription'):
            return JsonResponse({'status': 'error', 'message': "Event description is required."}, status=500)
        if not request.data.get('start')['dateTime']:
            return JsonResponse({'status': 'error', 'message': "Event start time is required."}, status=500)
        if not request.data.get('end')['dateTime']:
            return JsonResponse({'status': 'error', 'message': "Event end time is required."}, status=500)
        if not request.data.get('location'):
            return JsonResponse({'status': 'error', 'message': "Center location is required."}, status=500)
        # Authenticate using the service account
        print(SERVICE_ACCOUNT_FILE)
        credentials = service_account.Credentials.from_service_account_file(  
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        
        # Build the Google Calendar service
        service = build('calendar', 'v3', credentials=credentials)

        # Event details
        event = {
            'summary': request.data.get('eventName'),
            'location': request.data.get('location'),
            'centerId': request.data.get('center_id'), 
            'description': request.data.get('eventDescription'),
            'start': {
                'dateTime': request.data.get('start')['dateTime']+":00Z",  # Specify in ISO format
                'timeZone': 'Europe/London',
            },
            'end': {
                'dateTime': request.data.get('end')['dateTime']+":00Z",   
                'timeZone': 'Europe/London',
            },
            # 'attendees': [
            #     {'email': 'driver@example.com'},
            # ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }

        try:
            # Call the Calendar API to create the event
            calendar_id = 'shinyuy9@gmail.com' #'primary'  # Use the primary calendar or specify another calendar ID
            created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

            return JsonResponse({'status': 'success', 'event': created_event}, status=201)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)



class GoogleCalendarEventsAPIView(APIView):
    permission_classes = [AllowAny]  # Adjust based on your authentication requirements
  
    def get(self, request):
        # Path to your service account file        
        # Scopes required to access calendar events
        # SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

        try:
            # Authenticate with service account
            credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            )
            service = build("calendar", "v3", credentials=credentials)

            # Call the Google Calendar API
            calendar_id = 'shinyuy9@gmail.com' #'primary'  # Use the primary calendar or specify another calendar ID
            now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
            events_result = service.events().list(
                calendarId=calendar_id, timeMin=now,
                maxResults=10, singleEvents=True,
                orderBy="startTime"
            ).execute()
            print(events_result)
            events = events_result.get("items", [])

            # Format the response
            formatted_events = [
                {
                    "summary": event.get("summary", "No Title"),
                    "start": event["start"].get("dateTime", event["start"].get("date")),
                    "end": event["end"].get("dateTime", event["end"].get("date")),
                    "location": event.get("location", "No Location Provided"),
                }
                for event in events
            ]

            return Response({
                "status": "success",
                "events": formatted_events,
            })
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e),
            }, status=500)
            
            
class GoogleCalendarFilteredEventsAPIView(APIView):
    permission_classes = [AllowAny]  # Adjust as needed

    def post(self, request):
        # Parse query parameters
        time_min = request.data.get("timeMin")
        time_max = request.data.get("timeMax")
        location = request.data.get("location")
        center_id = request.data.get("centerId")
        
        
        if not center_id:
            raise NotFound({"error": "centerId parameter is required"})
        
        try:
            center = Center.objects.get(id=center_id)
            
        
            print(location)
            if not time_min:
                raise ValidationError({"error": "Date is required."})
            if not time_max:
                raise ValidationError({"error": "Date is required."})

            # Scopes for Google Calendar API

            try:
                # Authenticate with Google
                credentials = service_account.Credentials.from_service_account_file(
                    SERVICE_ACCOUNT_FILE, scopes=SCOPES
                )
                service = build("calendar", "v3", credentials=credentials)

                calendar_id = center.center_calendar_id #'shinyuy9@gmail.com' #'primary'
                # Fetch events for the specified date range
                events_result = service.events().list(
                    calendarId=calendar_id,
                    timeMin=time_min,
                    timeMax=time_max,
                    singleEvents=True,
                    orderBy="startTime"
                ).execute()
            

                events = events_result.get("items", [])

                # Filter events by location, if provided
                if location:
                    filtered_events = [event for event in events if event.get('location') == location]

                # Format the response
                formatted_events = [
                    {
                    "summary": event.get("summary", "No Title"),
                    "start": event["start"].get("dateTime", event["start"].get("date")),
                    "end": event["end"].get("dateTime", event["end"].get("date")),
                    "location": event.get("location", "No Location Provided"),
                    }
                    for event in filtered_events
                ]

                print(formatted_events)
                return Response({
                "status": "success",
                "events": formatted_events,
                })
            except Exception as e:
                return Response({
                "status": "error",
                "message": str(e),
            }, status=500)    
            
        except Center.DoesNotExist:
            raise NotFound({"error": f"Center with centerId '{center_id}' does not exist"})         
            
 
class GoogleCalendarGetFreeSlotsAPIView(APIView):
    permission_classes = [AllowAny]  # Adjust based on your authentication requirements
    def post(self, request):  
        # token = request.headers.get("Authorization").split("Bearer ")[1]
        # if not token:
        #     return Response({"error": "Authorization token missing"}, status=401)

        # # creds = Credentials(token)
        credentials = service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE, scopes=SCOPES
            )
        service = build("calendar", "v3", credentials=credentials)

        # Define the time range for free/busy check
        time_min = request.data.get("timeMin")
        time_max = request.data.get("timeMax")
        location = request.data.get("location")
        center_id = request.data.get("centerId")
        
        
        if not center_id:
            raise NotFound({"error": "centerId parameter is required"})
        
        try:
            center = Center.objects.get(id=center_id)

            # Free/Busy Query
            body = {
                "timeMin": time_min,
                "timeMax": time_max,
                "timeZone": "UTC",
                "items": [{"id": "shinyuy9@gmail.com"}],
            }
            events_result = service.freebusy().query(body=body).execute()
            busy_times = events_result["calendars"]["shinyuy9@gmail.com"]["busy"]

            # Calculate free slots
            free_slots = []
            current_start = time_min
            for busy in busy_times:
                free_slots.append({"start": current_start, "end": busy["start"]})
                current_start = busy["end"]

            free_slots.append({"start": current_start, "end": time_max})
            all_intervals = generate_working_hour_intervals(free_slots)

            return Response(all_intervals) 
        except Center.DoesNotExist:
            raise NotFound({"error": f"Center with centerId '{center_id}' does not exist"})           
            


def generate_working_hour_intervals(free_slots, working_start="08:00 AM", working_end="05:00 PM"):
    # Define working hours as datetime.time objects
    working_start = datetime.strptime(working_start, "%I:%M %p").time()
    working_end = datetime.strptime(working_end, "%I:%M %p").time()

    intervals = []
    for slot in free_slots:
        # Parse ISO 8601 start and end times
        start_time = datetime.fromisoformat(slot["start"].replace("Z", "+00:00"))
        end_time = datetime.fromisoformat(slot["end"].replace("Z", "+00:00"))

        # Adjust the slot to fit within working hours
        if start_time.time() < working_start:
            start_time = start_time.replace(hour=working_start.hour, minute=working_start.minute)
        if end_time.time() > working_end:
            end_time = end_time.replace(hour=working_end.hour, minute=working_end.minute)

        # Skip slots entirely outside working hours
        if start_time >= end_time:
            continue

        # Generate 15-minute intervals within the adjusted slot
        while start_time + timedelta(minutes=15) <= end_time:
            interval_end = start_time + timedelta(minutes=15)
            intervals.append(f"{start_time.strftime('%I:%M %p')} - {interval_end.strftime('%I:%M %p')}")
            start_time = interval_end

    return intervals