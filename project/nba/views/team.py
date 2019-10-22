import json
from rest_framework import viewsets, serializers, decorators, response
from rest_framework.permissions import AllowAny
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from .common import CommonMixin, StatField, PlayersField
from nba.models import Team


class TeamSerializer(serializers.ModelSerializer):
    stats = StatField(source='*')

    class Meta:
        model = Team
        fields = '__all__'


class TeamDetailSerializer(TeamSerializer, serializers.ModelSerializer):
    players = PlayersField(source='affiliations')


class TeamFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Team
        fields = '__all__'


class TeamViewSet(CommonMixin, viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = TeamFilter
    ordering_fields = ('name', )

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        return TeamDetailSerializer if self.action == 'retrieve' else serializer_class

    @decorators.list_route(methods=['get'], permission_classes=[AllowAny, ],)
    def coordinates(self, request):
        with open('nba/static/cities.json', 'r') as file:
            cities = [{**city, 'id': self.queryset.get(name=city['name']).id} for city in json.load(file)]
            return response.Response(cities)
