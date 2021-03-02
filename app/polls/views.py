from django.shortcuts import render
from .models import TaxiService
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Create your views here.
from django.http import HttpResponse

@require_http_methods(['GET'])
def index(request):
    queryset = TaxiService.objects.all()

    data = []

    for service in queryset:
        data.append(
            {
                'id': service.id,
                'vendorID': service.vendorID,
                'tpep_pickup_datetime': service.tpep_pickup_datetime,
                'tpep_dropoff_datetime': service.tpep_dropoff_datetime,
                'passenger_count': service.passenger_count,
                'trip_distance': service.trip_distance,
                'ratecodeID': service.ratecodeID,
                'store_and_fwd_flag': service.store_and_fwd_flag,
                'PULocationID': service.PULocationID,
                'DOLocationID': service.DOLocationID,
                'payment_type': service.payment_type,
                'fare_amount': service.fare_amount,
                'extra': service.extra,
                'mta_tax': service.mta_tax,
                'tip_amount': service.tip_amount,
                'tolls_amount': service.tolls_amount,
                'improvement_surcharge': service.improvement_surcharge,
                'total_amount': service.total_amount,
                'congestion_surcharge': service.congestion_surcharge
            }
        )

    obj = {
        'servicios': data
    }
    #return HttpResponse("Hello, world. You're at the polls index.")
    return JsonResponse(obj, safe=False)
