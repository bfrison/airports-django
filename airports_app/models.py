import json
from django.db import models

class Airport(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=127)
    city = models.CharField(max_length=127)
    country = models.CharField(max_length=127)
    elevation = models.IntegerField()
    latitude = models.DecimalField(max_digits=4, decimal_places=2)
    longitude = models.DecimalField(max_digits=5, decimal_places=2)
    def to_json(self):
        json_object = dict()
        json_object['code'] = self.code
        json_object['name'] = self.name
        json_object['city'] = self.city
        json_object['country'] = self.country
        json_object['elevation'] = str(self.elevation)
        json_object['latitude'] = str(self.latitude)
        json_object['longitude'] = str(self.longitude)
        return json_object
