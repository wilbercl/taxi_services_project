from django.db import models
from .constant import *

# Create your models here.
class TaxiService(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    VendorID = models.PositiveSmallIntegerField(null=True, choices=VENDOR_ID_CHOICES)
    tpep_pickup_datetime = models.DateTimeField(db_index=True, blank=False)
    tpep_dropoff_datetime = models.DateTimeField(blank=False)
    passenger_count = models.IntegerField(null=False)
    trip_distance = models.FloatField(null=False)
    RatecodeID = models.PositiveSmallIntegerField(choices=RATE_CODE_ID_CHOICES, null=False)
    store_and_fwd_flag = models.CharField(max_length=50, null=False)
    PULocationID = models.IntegerField(null=False)
    DOLocationID = models.IntegerField(null=False)
    payment_type = models.PositiveSmallIntegerField(choices=PAYMENT_TYPE_CHOICES, null=False)
    fare_amount =models.FloatField(null=False)
    extra = models.FloatField(null=False)
    mta_tax = models.FloatField(null=False)
    tip_amount = models.FloatField(null=False)
    tolls_amount = models.FloatField(null=False)
    improvement_surcharge =models.FloatField(null=False)
    total_amount = models.FloatField(null=False)
    congestion_surcharge = models.FloatField(null=False)