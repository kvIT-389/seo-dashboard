from django.db import connection

from django.db import models

from .metrika_handler import MetrikaHandler
from .topvisor_handler import TopvisorHandler

from dashboard_api.models import *

import datetime


class DatabaseHandler:
    def __init__(self) -> None:
        self._load_methods = {
            "visits": self.load_visits,
            "positions": self.load_positions,
            "tops": self.load_tops
        }

    def __new__(cls):
        """
        Re-define __new__ method to implement Singleton pattern.
        """

        if not hasattr(cls, "instance"):
            cls.instance = super(DatabaseHandler, cls).__new__(cls)

        return cls.instance

    @classmethod
    def _filter_dates(cls, data: list[dict], model: models.Model):
        loaded_dates = list(map(
            lambda date: date.strftime("%Y-%m-%d"),
            model.objects.dates("date", "day")
        ))

        return list(filter(
            lambda d: d.get("date") not in loaded_dates, data
        ))

    def load_data(self, data_section: str, **kwargs):
        load_method = self._load_methods.get(data_section)

        if (load_method is None):
            return []

        return load_method(**kwargs)

    def load_visits(self, **kwargs):
        data = MetrikaHandler().get_data(
            "visits", **kwargs
        )

        return Visits.load(
            self._filter_dates(data, Visits)
        )

    def load_positions(self, **kwargs):
        data = TopvisorHandler().get_positions(
            self.get_regions_indexes()
        )

        return Position.load(
            self._filter_dates(data, Position)
        )

    def load_tops(self, **kwargs):
        data = TopvisorHandler().get_tops(
            self.get_regions_indexes()
        )

        return SearchResultsTop.load(
            self._filter_dates(data, SearchResultsTop)
        )

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

        mods: dict[str, models.Model] = {
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
