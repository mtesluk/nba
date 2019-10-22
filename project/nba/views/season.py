import os
from rest_framework import viewsets, serializers, decorators, response
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from .common import StatSeasonField, PermissionMixin
from nba.models import Season
from nba.stat_config import common_stats, player_stat, team_stat, match_stat
from django.conf import settings


class SeasonSerializer(serializers.ModelSerializer):
    stats = StatSeasonField(source='*')

    class Meta:
        model = Season
        fields = '__all__'


class SeasonFilter(filters.FilterSet):
    class Meta:
        model = Season
        fields = '__all__'


class SeasonViewSet(PermissionMixin, viewsets.ModelViewSet):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = SeasonFilter

    def get_serializer_context(self):
        return {
            "player": self.request.GET.get('player', None),
            "team": self.request.GET.get('team', None)
        }

    @decorators.list_route(
        methods=['get']
    )
    def available_data(self, request):
        seasons_path = os.path.join(settings.BASE_DIR, 'data')
        matches_seasons = os.listdir(seasons_path + '/matches-json')
        stats_seasons = os.listdir(seasons_path + '/stats')
        return response.Response([season for season in matches_seasons if season in stats_seasons])
