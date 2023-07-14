from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from dashboard.datahandler.metrika_handler import MetrikaHandler
from dashboard.datahandler.topvisor_handler import TopvisorHandler


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "index.html")

def get_data(
    request: HttpRequest,
    data_section: str
) -> JsonResponse:
    return JsonResponse(
        MetrikaHandler().get_data(
            data_section,
            **request.GET
        )
    )
