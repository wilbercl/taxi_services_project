from django.shortcuts import render, redirect

from services.models import TaxiService
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

from taxi_services_project.settings import DEFAULT_IPP


@require_http_methods(['GET'])
def index(request):
    queryset = TaxiService.objects.filter(vendor_id=None)

    ipp = request.GET.get('ipp', DEFAULT_IPP)
    page = request.GET.get('page', 1)

    paginator = Paginator(queryset, ipp)

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    return render(request, 'services/index.html', {
        'items': items
    })


@require_http_methods(['GET'])
def longest_trips(request):
    vendor_id = int(request.GET.get('vendor_id', 1))
    limit = int(request.GET.get('limit', 2))

    queryset = list(
        TaxiService.objects.filter(vendor_id=vendor_id)
            .values('vendor_id', 'tpep_pickup_datetime', 'tpep_dropoff_datetime', 'trip_distance')
            .order_by('-trip_distance')[:limit]
    )

    obj = {
        'servicios': queryset,
    }

    return JsonResponse(obj, safe=False)


@csrf_exempt
@require_http_methods(['POST'])
def update_vendor_id(request):
    values = request.POST.getlist('vendor')  # ['vendor_id-id', ...]
    data_list = []

    for value in values:
        value = value.split('-')
        servicio_taxi = TaxiService.objects.get(id=value[1])
        servicio_taxi.vendor_id = value[0]
        data_list.append(servicio_taxi)

    TaxiService.objects.bulk_update(data_list, ['vendor_id'])

    return redirect('index')


