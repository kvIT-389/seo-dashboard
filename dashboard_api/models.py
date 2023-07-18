from django.core.exceptions import FieldError

from django.db import models
from django.db.utils import IntegrityError


"""
Abstract base models
"""

class LoadedModel(models.Model):
    """
    Model which contain load(data, ...) class method which
    allow to load new data stored in data parameter
    to appropriate DB table.
    """

    class Meta:
        abstract = True

    @classmethod
    def load(cls, data: list[dict[str]]):
        return []


class UniqueFieldModel(LoadedModel):
    """
    Model with exactly one (except id) unique field named 'name'.

    class SomeModel(UniqueFieldModel):
        field = models.Field(
            unique=True,
            ...
        )

        ...
    """

    class Meta:
        abstract = True

    @classmethod
    @property
    def field_name(cls) -> str:
        return cls._meta.fields[-1].name

    @classmethod
    def load(cls, data: list[dict[str]]):
        exceptions = super().load(data)

        for d in data:
            try:
                cls.objects.update_or_create(
                    **{
                        cls.field_name: d.get(cls.field_name)
                    }
                )

            except (IntegrityError, FieldError, ValueError) as e:
                exceptions.append(e)

        return exceptions


class FieldAutoLoadModel(LoadedModel):
    """
    Model which contains a referred fields (ForeignKey)
    and automatically load its models when self load(...) called.
    """

    class Meta:
        abstract = True
        unique_together = []

    @classmethod
    def load(cls, data: list[dict[str]]):
        for model in cls.fields_models.values():
            model.load(data)

        exceptions = super().load(data)

        for d in data:
            try:
                for (field_name, model) in cls.fields_models.items():
                    if (d.get(field_name) is None):
                        continue

                    d[field_name] = model.objects.get(
                        **{
                            field_name: d[field_name]
                        }
                    )

                cls.objects.update_or_create(
                    d, **{
                        key: d.get(key)
                        for key in cls._meta.unique_together[0]
                    }
                )

            except (IntegrityError, FieldError, ValueError) as e:
                exceptions.append(e)

        return exceptions

    @classmethod
    @property
    def fields_models(cls):
        return {}

"""
Models inherited from LoadedModel
"""

class SearchResultsTop(LoadedModel):
    date = models.DateField()
    region_index = models.PositiveIntegerField()
    value = models.PositiveIntegerField()

    class Meta:
        db_table = "search_results_tops"
        unique_together = [
            "date",
            "region_index"
        ]

    @classmethod
    def load(cls, data: list[dict[str]]):
        exceptions = super().load(data)

        for d in data:
            try:
                SearchResultsTop.objects.update_or_create(**d)

            except (IntegrityError, FieldError, ValueError) as e:
                exceptions.append(e)

        return exceptions

"""
Models inherited from UniqueFieldModel
"""

class TrafficSource(UniqueFieldModel):
    traffic_source = models.CharField(
        max_length=50, unique=True
    )

    class Meta:
        db_table = "traffic_sources"


class DeviceCategory(UniqueFieldModel):
    device_category = models.CharField(
        max_length=20, unique=True
    )

    class Meta:
        db_table = "device_categories"


class SearchEngine(UniqueFieldModel):
    search_engine = models.CharField(
        max_length=50, unique=True
    )

    class Meta:
        db_table = "search_engines"


class SearchPhrase(UniqueFieldModel):
    search_phrase = models.TextField(
        unique=True
    )

    class Meta:
        db_table = "search_phrases"


class Goal(UniqueFieldModel):
    goal = models.TextField(
        unique=True
    )

    class Meta:
        db_table = "goals"

"""
Models inherited from FieldAutoLoadModel
"""

class Visits(FieldAutoLoadModel):
    date = models.DateField()
    traffic_source = models.ForeignKey(
        to=TrafficSource,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    device_category = models.ForeignKey(
        to=DeviceCategory,
        on_delete=models.PROTECT
    )
    search_engine = models.ForeignKey(
        to=SearchEngine,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    search_phrase = models.ForeignKey(
        to=SearchPhrase,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    goal = models.ForeignKey(
        to=Goal,
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )
    visits = models.PositiveIntegerField()
    new_users = models.PositiveIntegerField()

    class Meta:
        db_table = "visits"
        unique_together = [
            "date",
            "traffic_source",
            "device_category",
            "search_engine",
            "search_phrase",
            "goal"
        ]

    @classmethod
    @property
    def fields_models(cls):
        return super().fields_models | dict(
            traffic_source=TrafficSource,
            device_category=DeviceCategory,
            search_engine=SearchEngine,
            search_phrase=SearchPhrase,
            goal=Goal
        )


class Position(FieldAutoLoadModel):
    project_id = models.PositiveIntegerField()
    search_phrase = models.ForeignKey(
        to=SearchPhrase,
        on_delete=models.PROTECT
    )
    date = models.DateField()
    region_index = models.PositiveIntegerField()
    position = models.PositiveIntegerField()

    class Meta:
        db_table = "site_positions"
        unique_together = [
            "search_phrase",
            "date",
            "region_index"
        ]

    @classmethod
    @property
    def fields_models(cls):
        return super().fields_models | dict(
            search_phrase=SearchPhrase,
        )
