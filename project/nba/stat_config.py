import copy


def _replace(list, *args):
    objs = copy.deepcopy(list)
    for obj in objs:
        for arg in args:
            if obj['name'] == arg['name']:
                obj['source'] = arg['source']
    return objs


common_stats = [
    {"name": "PTS", "type": "int", "source": "PTS", "hint": "Total points scored"},
    {"name": "FG%", "type": "float", "source": "FG%", "hint": "Shooting percentage"},
    {"name": "3P%", "type": "float", "source": "3P%", "hint": "3PT shooting percentage"},
    {"name": "FT%", "type": "float", "source": "FT%", "hint": "Free Throws shooting percentage"},
    {"name": "ORB", "type": "int", "source": "ORB", "hint": "Total offensive rebounds"},
    {"name": "DRB", "type": "int", "source": "DRB", "hint": "Total defensive rebounds"},
    {"name": "AST", "type": "int", "source": "AST", "hint": "Total assists"},
    {"name": "STL", "type": "int", "source": "STL", "hint": "Total steals"},
    {"name": "BLK", "type": "int", "source": "BLK", "hint": "Total blocks"},
    {"name": "TOV", "type": "int", "source": "TOV", "hint": "Total turnovers"},
    {"name": "PF", "type": "int", "source": "PF", "hint": "Total personal faults"}
]

player_stat = [
    *common_stats,
    {"name": "G", "type": "int", "source": "G", "hint": "Total games played"},
    {"name": "GS", "type": "int", "source": "GS", "hint": "Total games played in starting 5"},
    {"name": "MP", "type": "int", "source": "MP", "hint": "Total minutes played"},
    {"name": "2P%", "type": "float", "source": "2P%", "hint": "2PT shooting percentage"},
    {"name": "eFG%", "type": "float", "source": "eFG%", "hint": "effective shooting percentage"},
    {"name": "TRB", "type": "int", "source": "TRB", "hint": "Total rebounds"},
    {"name": "PER", "type": "float", "source": "PER", "hint": "Player efficiency rating"},
    {"name": "TS%", "type": "float", "source": "TS%", "hint": "True Shooting percentage"},
    {"name": "USG%", "type": "float", "source": "USG%", "hint": "Usage percentage"},
    {"name": "OWS", "type": "float", "source": "OWS", "hint": "Offensive win shares"},
    {"name": "DWS", "type": "float", "source": "DWS", "hint": "Defensive win shares"},
    {"name": "WS", "type": "float", "source": "WS", "hint": "Win shares"},
    {"name": "OBPM", "type": "float", "source": "OBPM", "hint": "Offensive box plus/minus"},
    {"name": "DBPM", "type": "float", "source": "DBPM", "hint": "Defensive box plus/minus"},
    {"name": "BPM", "type": "float", "source": "BPM", "hint": "Total box plus/minus"},
    {"name": "VORP", "type": "float", "source": "VORP", "hint": "Value over Replacement Player"}
]

team_stat = [
    *common_stats,
    {"name": "G", "type": "int", "source": "G", "hint": "Total games played"},
    {"name": "W", "type": "int", "source": "W", "hint": "Total wins"},
    {"name": "L", "type": "int", "source": "L", "hint": "Total losses"},
    {"name": "2P%", "type": "float", "source": "2P%", "hint": "2PT shooting percentage"},
    {"name": "TRB", "type": "int", "source": "TRB", "hint": "Total rebounds"},
    {"name": "ORtg", "type": "float", "source": "ORtg", "hint": "Offensive rating"},
    {"name": "DRtg", "type": "float", "source": "DRtg", "hint": "Defensive rating"},
    {"name": "NRtg", "type": "float", "source": "NRtg", "hint": "Net rating"},
    {"name": "Pace", "type": "float", "source": "Pace", "hint": "Pace rating - posessions per match"},
    {"name": "TS%", "type": "float", "source": "TS%", "hint": "True Shooting percentage"},
    {"name": "OeFG%", "type": "float", "source": "eFG%", "hint": "Offensive eFG percentage"},
    {"name": "DeFG%", "type": "float", "source": "OPP_eFG%", "hint": "Defensive eFG percentage"},
    {"name": "OTOV%", "type": "float", "source": "TOV%", "hint": "Offensive TOV percentage"},
    {"name": "ORB%", "type": "float", "source": "ORB%", "hint": "Offensive rebounds percentage"},
    {"name": "DTOV%", "type": "float", "source": "OPP_TOV%", "hint": "Defensive TOV percentage"},
    {"name": "DRB%", "type": "float", "source": "OPP_DRB%", "hint": "Defensive rebounds percentage"}
]

match_stat = [
    *_replace(common_stats, {"name": "FG%", "source": "FG_PCT"},
                            {"name": "ORB", "source": "OREB"},
                            {"name": "DRB", "source": "DREB"},
                            {"name": "3P%", "source": "FG3_PCT"},
                            {"name": "FT%", "source": "FT_PCT"}),
    {"name": "PLUS_MINUS", "type": "int", "source": "PLUS_MINUS", "hint": "Point difference"},
    {"name": "WL", "type": "string", "source": "WL", "hint": "Winner or loser"}
]
