from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.season import SeasonViewSet
from .views.matches import MatchViewSet
from .views.match_stat import MatchStatViewSet
from .views.player import PlayerViewSet
from .views.player_stat import PlayerStatViewSet
from .views.team import TeamViewSet
from .views.team_stat import TeamStatViewSet
from .views.admin import AdminView


router = DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'player_stats', PlayerStatViewSet)
router.register(r'matches', MatchViewSet)
router.register(r'match_stats', MatchStatViewSet)
router.register(r'teams', TeamViewSet)
router.register(r'team_stats', TeamStatViewSet)
router.register(r'seasons', SeasonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin', AdminView.as_view())
]
