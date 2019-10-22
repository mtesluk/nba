from rest_framework import viewsets, serializers
from nba.models import PlayerStat
from django_filters import rest_framework as filters


class PlayerStatFilter(filters.FilterSet):
    class Meta:
        model = PlayerStat
        fields = ('player', 'season', 'stat', 'value')


class PlayerStatSerializer(serializers.ModelSerializer):
    player = serializers.CharField(source="player.name")
    stat = serializers.CharField(source="stat.name")
    season = serializers.CharField(source="season.name")

    class Meta:
        model = PlayerStat
        fields = '__all__'


class PlayerStatViewSet(viewsets.ModelViewSet):
    queryset = PlayerStat.objects.all()
    serializer_class = PlayerStatSerializer
    filterset_class = PlayerStatFilter
