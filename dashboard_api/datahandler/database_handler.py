import datetime

from django.db import models

from .metrika_handler import MetrikaHandler
from .topvisor_handler import TopvisorHandler

from dashboard_api.models import SearchResultsTop, Visits, Position


class DatabaseHandler:
    def __init__(self) -> None:
        self._load_methods = {
            "visits": self.load_visits,
            "positions": self.load_positions,
            "tops": self.load_tops
        }

        self._specific_params = {
            "new_users": {
                "model": Visits,
                "group_by": {
                    "fields": ("date", ),
                    "aggregates": {
                        "visits": models.Sum("visits"),
                        "new_users": models.Sum("new_users")
                    }
                },
                "order_by": ("date", )
            },
            "traffic_sources": {
                "model": Visits,
                "group_by": {
                    "fields": ("traffic_source", ),
                    "aggregates": {
                        "visits": models.Sum("visits")
                    }
                },
                "order_by": ("-visits", )
            },
            "device_categories": {
                "model": Visits,
                "group_by": {
                    "fields": ("device_category", ),
                    "aggregates": {
                        "visits": models.Sum("visits")
                    }
                },
                "order_by": ("-visits", )
            },
            "search_engines": {
                "model": Visits,
                "group_by": {
                    "fields": ("date", "search_engine"),
                    "aggregates": {
                        "visits": models.Sum("visits")
                    }
                },
                "order_by": ("search_engine", "date")
            },
            "search_phrases": {
                "model": Visits,
                "group_by": {
                    "fields": ("search_phrase", ),
                    "aggregates": {
                        "visits": models.Sum("visits")
                    }
                },
                "order_by": ("-visits", )
            },
            "goals": {
                "model": Visits,
                "group_by": {
                    "fields": ("date", "goal"),
                    "aggregates": {
                        "visits": models.Sum("visits")
                    }
                },
                "order_by": ("date", )
            },
            "positions": {
                "model": Position,
                "group_by": {
                    "fields": ("date", "search_phrase"),
                    "aggregates": {
                        "position": models.Avg("position")
                    }
                },
                "order_by": ("date", "position")
            },
            "tops": {
                "model": SearchResultsTop,
                "order_by": ("date", )
            }
        }

    def __new__(cls):
        """
        Re-define __new__ method to implement Singleton pattern.
        """

        if not hasattr(cls, "instance"):
            cls.instance = super(DatabaseHandler, cls).__new__(cls)

        return cls.instance

    @staticmethod
    def _filter_dates(data: list[dict], model: models.Model):
        loaded_dates = list(map(
            lambda date: date.isoformat(),
            model.objects.dates("date", "day")
        ))

        today = datetime.date.today().isoformat()

        return list(filter(
            lambda d: d.get("date") == today or \
                      d.get("date") not in loaded_dates, data
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
            TopvisorHandler().get_regions_indexes(),
            **kwargs
        )

        return Position.load(
            self._filter_dates(data, Position)
        )

    def load_tops(self, **kwargs):
        data = TopvisorHandler().get_tops(
            TopvisorHandler().get_regions_indexes(),
            **kwargs
        )

        return SearchResultsTop.load(
            self._filter_dates(data, SearchResultsTop)
        )

    def get_data(
        self,
        data_section: str,
        **kwargs
    ) -> (models.QuerySet | None):
        if (data_section not in self._specific_params):
            return

        today = datetime.date.today().strftime("%Y-%m-%d")

        dates_filtered = self._specific_params.get(
            data_section, {}
        ).get(
            "model"
        ).objects.filter(
            date__range=[
                kwargs.get("date1", [today])[0],
                kwargs.get("date2", [today])[0]
            ]
        ).order_by(
            *self._specific_params.get(
                data_section, {}
            ).get(
                "order_by"
            )
        )

        if (data_section == "tops"):
            qs = dates_filtered.values("date")

            max_value = qs.aggregate(
                max_value=models.Max("value")
            ).get("max_value")

            return qs.annotate(
                percentage=models.Avg("value") * 100 / max_value
            )

        return dates_filtered.group_by(
            **self._specific_params.get(
                data_section
            ).get("group_by")
        )
