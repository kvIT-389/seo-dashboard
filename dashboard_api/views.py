from django.http import HttpRequest, HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt

from rest_framework import serializers

from .models import *
from .serializers import dashboard_api_serializers

from .datahandler.database_handler import DatabaseHandler


@csrf_exempt
def get_data(request: HttpRequest, data_section: str):
    if(request.method == "GET"):
        serializer = dashboard_api_serializers.get(
            data_section, serializers.Serializer
        )(
            instance=DatabaseHandler().get_data(
                data_section, **request.GET
            ),
            many=True
        )

        return JsonResponse(
            dict(data=serializer.data),
            status=201
        )

    return HttpResponse(
        "POST request method is not allowed.",
        status=400
    )

def load_data(request: HttpRequest, data_section: str):
    errors = DatabaseHandler().load_data(
        data_section, **request.GET
    )

    return JsonResponse(dict(
        exceptions=list(map(lambda e: str(e), errors))
    ))

def count(request: HttpRequest):
    return JsonResponse({
        "records_count": {
            model._meta.db_table: model.objects.count()
            for model in (
                Visits,
                Position,
                TrafficSource,
                DeviceCategory,
                SearchEngine,
                SearchPhrase,
                Goal,
                SearchResultsTop
            )
        }
    })
