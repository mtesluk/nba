from random import randint
from rest_framework import serializers, response, decorators, pagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models.functions import Cast
from django.db.models.expressions import Case, When, Q
from django.db.models import FloatField
from nba.stat_config import common_stats, player_stat, team_stat, match_stat


class AdditionalView:
    def get_serializer_context(self):
        return {"season": self.request.GET.get('season', None)}


class FiltersAndOrderingMixin:
    def _season_filter(self, queryset, season):
        return queryset.exclude(~Q(stats__season=season))

    def _stats_order(self, queryset, season, order_name):
        if order_name.replace('-', '') not in self.ordering_fields:
            stats = self.get_queryset().model.stats.rel.related_model.objects \
                .filter(stat__name=order_name.replace('-', ''), season=season) \
                .annotate(sort_value=Cast('value', output_field=FloatField())) \
                .order_by('sort_value' if '-' not in order_name else '-sort_value')

            try:
                queryset = queryset.order_by(Case(
                    *[When(id=stat.player.id, then=i) for i, stat in enumerate(stats)])
                )
            except:
                queryset = queryset.order_by(Case(
                    *[When(id=stat.team.id, then=i) for i, stat in enumerate(stats)])
                )

        return queryset

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        season = self.request.GET.get('season', None)
        order_name = self.request.GET.get('ordering', '')

        queryset = self._season_filter(queryset, season)
        queryset = self._stats_order(queryset, season, order_name)

        return queryset


class HintMixin:
    @decorators.list_route(
        methods=['get'],
        permission_classes=[AllowAny, ],)
    def hints(self, request, format=None):
        type = self.get_queryset().model._meta.model_name + '_stat'
        data = [{'name': stat['name'], 'hint': stat['hint']} for stat in globals()[type]]
        return response.Response(data)


class StatSeasonField(serializers.Field):
    def to_representation(self, value):
        data = []
        if self.context.get('player'):
            data = {stat.stat.name: (float(stat.value) if '.' in stat.value else int(stat.value))
                    for stat in value.player_stats.filter(season=value.id, player=self.context.get('player'))}
        elif self.context.get('team'):
            data = {stat.stat.name: (float(stat.value) if '.' in stat.value else int(stat.value))
                    for stat in value.team_stats.filter(season=value.id, team=self.context.get('team'))}
        return data


class RandomBetField(serializers.Field):
    def to_representation(self, value):
        return randint(1, 100)


class StatField(serializers.Field):
    def to_representation(self, value):
        stats = {stat.stat.name: (float(stat.value) if '.' in stat.value else int(stat.value))
                 for stat in value.stats.filter(season=self.context.get('season'))}
        stats['bet%'] = randint(1, 100)
        return stats


class MatchField(serializers.Field):
    def to_representation(self, value):
        host_stat = {}
        visitor_stat = {}
        for stat in value.match_stats.filter(team=value.team_host):
            if '.' in stat.value:
                host_stat[stat.stat.name] = float(stat.value)
            elif 'WL' in stat.stat.name:
                host_stat[stat.stat.name] = str(stat.value)
            else:
                host_stat[stat.stat.name] = int(stat.value)
        for stat in value.match_stats.filter(team=value.team_visitor):
            if '.' in stat.value:
                visitor_stat[stat.stat.name] = float(stat.value)
            elif 'WL' in stat.stat.name:
                visitor_stat[stat.stat.name] = str(stat.value)
            else:
                visitor_stat[stat.stat.name] = int(stat.value)
        data = [{'team_host_stats': host_stat, 'team_visitor_stats': visitor_stat}]
        return data


class TeamsField(serializers.Field):
    def to_representation(self, value):
        data = []
        for affiliation in value.filter(season=self.context.get('season')):
            for team in affiliation.teams.all():
                data.append({'name': team.name, 'id': team.id})
        return data


class PlayersField(serializers.Field):
    def to_representation(self, value):
        data = []
        for affiliation in value.filter(season=self.context.get('season')).select_related('player'):
            data.append({'name': affiliation.player.name, 'id': affiliation.player.id})
        return data


class DefaultPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PermissionMixin:
    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [IsAuthenticated],
        'create': [IsAuthenticated],
        'update': [IsAuthenticated],
    }

    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class CommonMixin(AdditionalView, FiltersAndOrderingMixin, HintMixin, PermissionMixin):
    pagination_class = DefaultPagination
