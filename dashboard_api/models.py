from django.db import models


class TrafficSource(models.Model):
    traffic_source = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "traffic_sources"


class DeviceCategory(models.Model):
    device_category = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = "device_categories"


class SearchEngine(models.Model):
    search_engine = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "search_engines"


class SearchPhrase(models.Model):
    search_phrase = models.TextField(unique=True)

    class Meta:
        db_table = "search_phrases"


class Goal(models.Model):
    goal = models.TextField(unique=True)

    class Meta:
        db_table = "goals"


class Visits(models.Model):
    date = models.DateField()
    traffic_source = models.ForeignKey(
        to=TrafficSource,
        on_delete=models.PROTECT,
        default=None,
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
        default=None,
        blank=True,
        null=True
    )
    search_phrase = models.ForeignKey(
        to=SearchPhrase,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True
    )
    goal = models.ForeignKey(
        to=Goal,
        on_delete=models.PROTECT,
        default=None,
        blank=True,
        null=True
    )
    visits = models.PositiveIntegerField()
    new_users = models.PositiveIntegerField()

    class Meta:
        db_table = "visits"
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "date",
                    "traffic_source",
                    "device_category",
                    "search_engine",
                    "search_phrase",
                    "goal"
                ),
                name="visits_unique_index"
            )
        ]


class Position(models.Model):
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
        constraints = [
            models.UniqueConstraint(
                fields=(
                    "search_phrase",
                    "date",
                    "region_index"
                ),
                name="positions_unique_index"
            )
        ]


class SearchResultsTop(models.Model):
    date = models.DateField()
    region_index = models.PositiveIntegerField()
    value = models.PositiveIntegerField()

    class Meta:
        db_table = "search_results_tops"
        constraints = [
            models.UniqueConstraint(
                fields=("date", "region_index"),
                name="search_result_unique_index"
            )
        ]
