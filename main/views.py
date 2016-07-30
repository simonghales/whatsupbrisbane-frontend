import json
import haversine

from django.shortcuts import render
from django.http import HttpResponse

from .models import EventInfo
from .utilities import *

# Create your views here.
def index(request):
    
    return render(request, 'index.html')

def db(request):

    newData = EventInfo()
    newData.title = "TestOne"
    newData.save()

    dbData = EventInfo.objects.all()
    
    return render(request, 'db.html', {'eventinfo': dbData})

def test(request):

    response = HttpResponse(json.dumps([{"name": "value", "lat": 333, "lng": 460, "description": "This is a nonsense response"}
                                        ,{"name": "value", "lat": 333, "lng": 460, "description": "This is a nonsense response"}
                                        ,{"name": "value", "lat": 333, "lng": 460, "description": "This is a nonsense response"}
                                        ,{"name": "value", "lat": 333, "lng": 460, "description": "This is a nonsense response"}
                                        ,{"name": "value", "lat": 333, "lng": 460, "description": "This is a nonsense response"}]))  
    response["Access-Control-Allow-Origin"] = "*"  
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"  
    response["Access-Control-Max-Age"] = "1000"  
    response["Access-Control-Allow-Headers"] = "*"  
    return response

def events(request):

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    lat = body['lat']
    lng = body['lng']
    current_location = (lat,lng)
    
    radius = body['radius']
    timeStart = body['start']
    timeEnd = body['end']

    # run function to retrieve from db and filter based on these
    # then return the results in a HttpResponse(json.dumps list

    allEvents = EventInfo.objects.all()
    selectedEvents = []

    for event in allEvents:
        event_location = findOrCreateLatLong(event.venueAddress)
        
        if(event.timeStart => timeStart and
           event.timeEnd <= timeEnd and
           haversine(event_location, current_location) < radius):

            selectedEvents.append({"name": event.title, "lat": event_location[0], "lng": event_location[1], "description": event.description})

    response = HttpResponse(json.dumps(selectedEvents))
    response["Access-Control-Allow-Origin"] = "*"  
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"  
    response["Access-Control-Max-Age"] = "1000"  
    response["Access-Control-Allow-Headers"] = "*"  
    return response
    
def allEvents(request):

    allEvents = EventInfo.objects.all()
    selectedEvents = []

    for event in allEvents:
        selectedEvents.append({"name": event.title, "lat": address.lat, "lng": address.lng, "description": event.description})
        
    response = HttpResponse(json.dumps(selectedEvents))
    response["Access-Control-Allow-Origin"] = "*"  
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"  
    response["Access-Control-Max-Age"] = "1000"  
    response["Access-Control-Allow-Headers"] = "*"  
    return response
    
