from django.shortcuts import render
from .models import TaxiService

from django.template import RequestContext, loader
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

from app.settings import DEFAULT_IPP

@require_http_methods(['GET'])
def index(request):
    # template = loader.get_template('polls/index.html')

    queryset = TaxiService.objects.filter(VendorID=1)

    ipp = request.GET.get('ipp', DEFAULT_IPP)
    paginator = Paginator(queryset, ipp)
    page = request.POST.get('page')

    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        items = paginator.page(paginator.num_pages)

    data = []

    for service in items:
        data.append(
            {
                'VendorID': service.VendorID,
                'tpep_pickup_datetime': service.tpep_pickup_datetime,
                'trip_distance': service.trip_distance,
                'payment_type': service.payment_type
            }
        )

    paginator = {
            'count': paginator.count,
            'ipp': ipp,
            'page': page,
            'has_previous': items.has_previous(),
            'has_next': items.has_next(),
            'num_pages': paginator.num_pages,
            'previous_page_number': items.previous_page_number(),
            'page_range': paginator.page_range,
            'number': items.number,
            'next_page_number': items.next_page_number()
    }

    obj = {
        # 'data': data,
        'paginator': paginator
    }

    # return JsonResponse(obj, safe=False)
    return render(request, 'polls/index.html', {
        'data': data,
        'paginator': paginator,
    })

    # context = RequestContext(request, {
    #     'meta_description': '',
    #     'meta_keywords': '',
    #     'items': items,
    # })
    #
    # return HttpResponse(template.render(context))

@require_http_methods(['GET'])
def longest_trips(request):
    vendor_id = int(request.GET.get('vendor_id', 5))
    limit = int(request.GET.get('limit', 2))

    queryset = TaxiService.objects.filter(VendorID=vendor_id).order_by('-trip_distance')[:limit]

    data = []

    for v_id in queryset:
        data.append(
            {
                'VendorID': v_id.VendorID,
                'tpep_pickup_datetime': v_id.tpep_pickup_datetime,
                'tpep_dropoff_datetime': v_id.tpep_dropoff_datetime,
                'trip_distance': v_id.trip_distance
            }
        )

    obj = {
        'servicios': data,
    }

    return JsonResponse(obj, safe=False)