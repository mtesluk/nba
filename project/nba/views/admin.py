from rest_framework import views
from rest_framework import response, decorators
from nba.tasks import download, insert

SEASON_TYPE_MAPPER = {
    'Regular Season': 'RS'
}


class AdminView(views.APIView):
    # permission_classes = (AllowAny, )

    def post(self, request):
        type = request.data.get('type', None)
        seasons = request.data.get('season', [])
        secondary_type = request.data.get('secondary_type', [])
        season_type = SEASON_TYPE_MAPPER[request.data.get('season_type', None)]
        if type == 'insert':
            insert.delay(seasons, season_type)
        elif type == 'download':
            for season in seasons:
                if 'Players and team stats' in secondary_type:
                    download.delay(season)
                if 'Matches' in secondary_type:
                    download.delay(season, season_type)
        return response.Response({'message': "Action '{}' is in progress".format(type)}, 200)
