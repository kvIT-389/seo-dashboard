from django.http import HttpRequest, JsonResponse

from .datahandler.metrika_handler import MetrikaHandler
from .datahandler.topvisor_handler import TopvisorHandler
from .datahandler.database_handler import DatabaseHandler

from .models import *


def get_data(
    request: HttpRequest,
    data_section: str
) -> JsonResponse:
    if (request.GET.get("source") == "ym"):
        return JsonResponse(
            MetrikaHandler().get_data(
                data_section,
                **request.GET
            )
        )

    if (request.GET.get("source") == "tv"):
        regions_indexes = TopvisorHandler().get_regions_indexes()
        return JsonResponse(
            dict(
                regions_indexes=regions_indexes,
                positions=TopvisorHandler().get_positions(
                    regions_indexes
                ),
                tops=TopvisorHandler().get_tops(
                    regions_indexes
                )
            )
        )

    if (data_section == "all"):
        return JsonResponse({
            "data": {
                "tops": [
                    *SearchResultsTop.objects.all().values()
                ],
                "positions": [
                    *Position.objects.all().values()
                ],
                "visits": [
                    *Visits.objects.all().values()
                ],
                "device_categories": [
                    *DeviceCategory.objects.all().values()
                ]
            }
        })

    return JsonResponse(
        DatabaseHandler().get_data(
            data_section, **request.GET
        )
    )

def load(
    request: HttpRequest,
    data_section: str
) -> JsonResponse:
    errors = []
    if (data_section == "visits"):
        errors = DatabaseHandler().load_visits(**request.GET)

    if (data_section == "positions"):
        errors = DatabaseHandler().load_positions()

    if (data_section == "tops"):
        errors = DatabaseHandler().load_tops()

    return JsonResponse(dict(
        exceptions=list(map(lambda e: str(e), errors))
    ))

def count(
    request: HttpRequest
) -> JsonResponse:
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
