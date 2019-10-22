from rest_framework import viewsets, serializers
from nba.models import Match
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from .common import PermissionMixin, MatchField, RandomBetField
import django_filters


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    season = serializers.StringRelatedField()
    team_host = serializers.StringRelatedField()
    team_visitor = serializers.StringRelatedField()
    host_bet = RandomBetField(source="*")
    stats = MatchField(source="*")

    class Meta:
        model = Match
        fields = ('id', 'season', 'season_type', 'date', 'team_host', 'team_visitor', 'stats', 'host_bet')


class MatchFilter(django_filters.FilterSet):
    season = filters.CharFilter(field_name='season')
    season_type = filters.CharFilter(field_name='season_type', lookup_expr='icontains')
    date = filters.CharFilter(field_name='date', lookup_expr='icontains')
    team_host = django_filters.CharFilter(field_name='team_host__name', lookup_expr='icontains')
    team_visitor = django_filters.CharFilter(field_name='team_visitor__name', lookup_expr='icontains')

    class Meta:
        model = Match
        fields = ('season', 'season_type', 'date', 'team_host', 'team_visitor')


class MatchViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter,)
    filter_class = MatchFilter
    ordering_fields = ('date', )
