from rest_framework import viewsets, serializers
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import api_view, permission_classes
from .common import CommonMixin, StatField, TeamsField
from nba.models import Player


class PlayerSerializer(serializers.ModelSerializer):
    stats = StatField(source='*')

    class Meta:
        model = Player
        fields = '__all__'


class PlayerDetailSerializer(serializers.ModelSerializer):
    teams = TeamsField(source='affiliations')

    class Meta:
        model = Player
        fields = '__all__'


class PlayerFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    age = filters.CharFilter(lookup_expr='icontains')
    position = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Player
        fields = '__all__'


class PlayerViewSet(CommonMixin, viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_class = PlayerFilter
    ordering_fields = ('name', 'position', 'age')

    def get_serializer_class(self):
        serializer_class = super().get_serializer_class()
        return PlayerDetailSerializer if self.action == 'retrieve' else serializer_class
