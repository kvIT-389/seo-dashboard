from rest_framework import serializers


class NewUsersSerializer(serializers.Serializer):
    date = serializers.DateField()
    visits = serializers.IntegerField()
    new_users = serializers.IntegerField()


class TrafficSourceSerializer(serializers.Serializer):
    traffic_source = serializers.CharField(
        source="traffic_source.traffic_source",
        allow_blank=True,
        allow_null=True
    )
    visits = serializers.IntegerField()


class DeviceCategorySerializer(serializers.Serializer):
    device_category = serializers.CharField(
        source="device_category.device_category"
    )
    visits = serializers.IntegerField()


class SearchEngineSerializer(serializers.Serializer):
    search_engine = serializers.CharField(
        source="search_engine.search_engine",
        allow_blank=True,
        allow_null=True
    )
    visits = serializers.IntegerField()


class SearchPhraseSerializer(serializers.Serializer):
    search_phrase = serializers.CharField(
        source="search_phrase.search_phrase",
        allow_blank=True,
        allow_null=True
    )
    visits = serializers.IntegerField()


class GoalSerializer(serializers.Serializer):
    date = serializers.DateField()
    goal = serializers.CharField(
        source="goal.goal",
        allow_blank=True,
        allow_null=True
    )
    visits = serializers.IntegerField()


class PositionsSerializer(serializers.Serializer):
    search_phrase = serializers.CharField(
        source="search_phrase.search_phrase"
    )
    date = serializers.DateField()
    region_index = serializers.IntegerField()
    position = serializers.IntegerField()


class SearchResultsTopSerializer(serializers.Serializer):
    date = serializers.DateField()
    region_index = serializers.IntegerField()
    percentage = serializers.IntegerField()


dashboard_api_serializers: dict[str, serializers.Serializer] = {
    "new_users": NewUsersSerializer,
    "traffic_sources": TrafficSourceSerializer,
    "device_categories": DeviceCategorySerializer,
    "search_engines": SearchEngineSerializer,
    "search_phrases": SearchPhraseSerializer,
    "goals": GoalSerializer,
    "positions": PositionsSerializer,
    "tops": SearchResultsTopSerializer
}
