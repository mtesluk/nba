from rest_framework import viewsets, serializers
from nba.models import MatchStat
from django_filters import rest_framework as filters


class MatchStatSerializer(serializers.ModelSerializer):
    match = serializers.StringRelatedField()
    team = serializers.CharField(source='team.name')
    stat = serializers.CharField(source='stat.name')

    class Meta:
        model = MatchStat
        fields = '__all__'


class MatchStatFilter(filters.FilterSet):
    class Meta:
        model = MatchStat
        fields = ('team', 'match', 'stat')


class MatchStatViewSet(viewsets.ModelViewSet):
    queryset = MatchStat.objects.all()
    serializer_class = MatchStatSerializer
    filterset_class = MatchStatFilter
