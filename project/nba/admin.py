from django.contrib import admin
from nba.models import *


class StatAdmin(admin.ModelAdmin):
    pass


class PlayerAdmin(admin.ModelAdmin):
    pass


class TeamAdmin(admin.ModelAdmin):
    pass


class AffiliationAdmin(admin.ModelAdmin):
    pass


class SeasonAdmin(admin.ModelAdmin):
    pass


class PlayerStatAdmin(admin.ModelAdmin):
    pass


class TeamStatAdmin(admin.ModelAdmin):
    pass


admin.site.register(Stat, StatAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Affiliation, AffiliationAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(PlayerStat, PlayerStatAdmin)
admin.site.register(TeamStat, TeamStatAdmin)
