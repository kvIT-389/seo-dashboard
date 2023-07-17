from django.core.exceptions import FieldError

from django.db import connection

from django.db.models import Model
from django.db.utils import IntegrityError

from .metrika_handler import MetrikaHandler
from .topvisor_handler import TopvisorHandler

from dashboard_api.models import *

import datetime


class DatabaseHandler:
    def __init__(self) -> None:
        pass

    def __new__(cls):
        """
        Re-define __new__ method to implement Singleton pattern.
        """

        if not hasattr(cls, "instance"):
            cls.instance = super(DatabaseHandler, cls).__new__(cls)

        return cls.instance

    def load_visits(self, **kwargs) -> list:
        deps: dict[str, Model] = {
            "traffic_source": TrafficSource,
            "device_category": DeviceCategory,
            "search_engine": SearchEngine,
            "search_phrase": SearchPhrase,
            "goal": Goal
        }

        objects: dict[str, dict[str, Model]] = {}

        for (data_section, model) in deps.items():
            data: list = MetrikaHandler().get_data(
                data_section, **dict(
                    date1=kwargs.get("date1", "today"),
                    date2=kwargs.get("date2", "today")
                )
            ).get("data", [])

            objects[data_section] = {}
            for d in data:
                obj = model.objects.get_or_create(
                    **{
                        data_section: d.get(data_section)
                    }
                )[0]
                objects[data_section][obj.__dict__.get(data_section)] = obj

        visits: list[dict] = MetrikaHandler().get_data(
            "visits", **kwargs
        ).get("data", [])

        exceptions = []

        for d in visits:
            try:
                for (data_section, data) in objects.items():
                    d[data_section] = data.get(d[data_section])

                Visits.objects.get_or_create(**d)

            except (IntegrityError, FieldError, ValueError) as e:
                exceptions.append(e)

        return exceptions

    def load_regions(self) -> list:
        return []

    def load_positions(self) -> list:
        positions: list[dict] = TopvisorHandler().get_positions(
            self.get_regions_indexes()
        )

        exceptions = []

        for d in positions:
            try:
                d["search_phrase"] = SearchPhrase.objects.get_or_create(
                    search_phrase=d.get("search_phrase")
                )[0]

                Position.objects.update_or_create(**d)

            except (IntegrityError, FieldError, ValueError) as e:
                exceptions.append(e)

        return exceptions

    def load_tops(self) -> list:
        data: list[dict] = TopvisorHandler().get_tops(
            self.get_regions_indexes()
        )

        exceptions = []

        for d in data:
            try:
                SearchResultsTop.objects.update_or_create(**d)

            except (IntegrityError, FieldError, ValueError) as e:
                exceptions.append(e)

        return exceptions

    def get_data(self, data_section: str, **kwargs) -> dict:
        today = datetime.date.today().strftime("%Y-%m-%d")

        date1: str = kwargs.get("date1", today)
        date2: str = kwargs.get("date2", today)

        if (data_section == "positions"):
            return {
                "data": [
                    *Position.objects.all().filter(
                        date__range=[date1, date2]
                    ).values()
                ]
            }

        if (data_section == "tops"):
            return {
                "data": [
                    *SearchResultsTop.objects.all().filter(
                        date__range=[date1, date2]
                    ).values()
                ]
            }

        mods: dict[str, Model] = {
            "traffic_source": TrafficSource,
            "device_category": DeviceCategory,
            "search_engine": SearchEngine,
            "search_phrase": SearchPhrase,
            "goal": Goal
        }

        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                    select D.{data_section}, sum(V.visits) as DV
                    from visits V
                    join {mods.get(data_section, DeviceCategory)._meta.db_table} D
                    on V.{data_section}_id=D.id
                    where V.date between %s and %s
                    group by D.{data_section}
                    order by DV desc
                """,
                [
                    kwargs.get("date1", today),
                    kwargs.get("date2", today)
                ]
            )

            data = list(cursor.fetchall())

        return {
            "data": [
                {
                    key: value for key, value in zip(
                        (data_section, "visits"), values
                    )
                }
                for values in data
            ]
        }

    def get_regions_indexes(self) -> list[int]:
        return TopvisorHandler().get_regions_indexes()
