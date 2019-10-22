from rest_framework import viewsets, serializers
from nba.models import TeamStat
from django_filters import rest_framework as filters


class TeamStatFilter(filters.FilterSet):
    class Meta:
        model = TeamStat
        fields = ('team', 'season', 'stat', 'value')


class TeamStatSerializer(serializers.ModelSerializer):
    team = serializers.CharField(source="team.name")
    stat = serializers.CharField(source="stat.name")
    season = serializers.CharField(source="season.name")

    class Meta:
        model = TeamStat
        fields = '__all__'


class TeamStatViewSet(viewsets.ModelViewSet):
    queryset = TeamStat.objects.all()
    serializer_class = TeamStatSerializer
    filterset_class = TeamStatFilter
