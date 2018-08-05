import json
from django.core import serializers
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from .models import Airport

def get_airports_json(request):
    if request.method == 'GET':
        airports = Airport.objects.order_by('code')
        data = json.dumps([airport.to_json() for airport in airports])
        return HttpResponse(data, status=200, content_type='application/json')
    elif request.method == 'POST':
        json_object = json.loads(request.body)
        airport = Airport.objects.create(**json_object)
        data = json.dumps(airport.to_json())
        response = HttpResponse(data, status=201)
        response['Location'] = reverse('airports_app:json', kwargs={'pk':airport.pk})
        return response

def get_airport_json(request, pk):
    if request.method == 'GET':
        airport = get_object_or_404(Airport, pk=pk)
        data = json.dumps(airport.to_json())
        return HttpResponse(data, content_type='application/json')
    elif request.method == 'DELETE':
        airport = get_object_or_404(Airport, pk=pk)
        airport.delete()
        return HttpResponse(status=204)
    elif request.method == 'PUT':
        # airport = get_object_or_404(Airport, pk=pk)
        # pk = airport.pk
        json_object = json.loads(request.body)
        json_object.update(pk=pk)
        # airport.__dict__.update(json_object)
        # airport.save()
        # data = json.dumps(airport.to_json())
        with connection.cursor() as cursor:
            cursor.execute('''UPDATE airports_app_airport
            SET CODE = %s, NAME = %s, CITY = %s, COUNTRY = %s, ELEVATION = %s, LATITUDE = %s, LONGITUDE = %s
            WHERE CODE = %s''', [json_object[key] for key in ['code','name','city','country','elevation','latitude','longitude','pk']])
        airport = get_object_or_404(Airport, pk=json_object['code'])
        data = json.dumps(airport.to_json())
        response = HttpResponse(data, status=201, content_type='application/json')
        response['Location'] = reverse('airports_app:json', kwargs={'pk':airport.pk})
        return response
