from django.shortcuts import render
from .models import TaxiService
from django.views.decorators.csrf import csrf_exempt

from django.template import RequestContext, loader
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

from taxi_services_project.settings import DEFAULT_IPP


@require_http_methods(['GET'])
def index(request):
    queryset = TaxiService.objects.filter(vendor_id=None)#.values('id', 'vendor_id', 'tpep_pickup_datetime', 'trip_distance', 'payment_type')

    ipp = request.GET.get('ipp', DEFAULT_IPP)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, ipp)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)

    # return JsonResponse(obj, safe=False)
    return render(request, 'services/index.html', {
        'items': items
    })


@require_http_methods(['GET'])
def longest_trips(request):
    vendor_id = int(request.GET.get('vendor_id', 5))
    limit = int(request.GET.get('limit', 2))

    queryset = (
        TaxiService.objects.filter(vendor_id=vendor_id)
            .values('vendor_id', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'trip_distance')
            .order_by('-trip_distance')[:limit]
    )

    data = []

    for v_id in queryset:
        data.append(
            {
                'vendor_id': v_id['vendor_id'],
                'tpep_pickup_datetime': v_id['tpep_pickup_datetime'],
                'tpep_dropoff_datetime': v_id['tpep_dropoff_datetime'],
                'trip_distance': v_id['trip_distance']
            }
        )

    obj = {
        'servicios': data,
    }

    return JsonResponse(obj, safe=False)


@csrf_exempt
@require_http_methods(['POST'])
def update_vendor_id(request):

    print(request.POST)
    # for key in request.__dict__['META'].keys():
    #     print(key)
    # if 'values' in request.POST:
    values = request.POST.get('vendor')  # [(id, vendor), ...]
    # data_list = []
    print(values)
    # print(values)
    # print('entro')


    # for value in values:
    #     print(value)
    #     # servicio_taxi = TaxiService.objects.get(id=value[0])
    #     #
    #     # if (value[1] == 'Creative Mobile Technologies, LLC'):
    #     #     servicio_taxi.vendor_id = 1
    #     # else:
    #     #     servicio_taxi.vendor_id = 2
    #     #
    #     # servicio_taxi.save()
    #     # #data_list.append(servicio_taxi)

    return JsonResponse({}, status=200)


