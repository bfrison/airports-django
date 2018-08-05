from django.urls import path

from . import views

app_name = 'airports_app'
urlpatterns = [
    path('json', views.get_airports_json, name='json_list'),
    path('json/<str:pk>', views.get_airport_json, name='json'),
]