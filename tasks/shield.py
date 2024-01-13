from typing import List
from game_message import CrewDistance, CrewMember, GameMessage
from station_util import get_station_position
from tasks.task import Task
from actions import CrewMoveAction, RadarScanAction

class ShieldTask(Task):

    def __init__(self):
        pass

    def get_action(self, game_message: GameMessage, crew: CrewMember):
        team_id = game_message.currentTeamId
        my_ship = game_message.ships.get(team_id)
        if my_ship.currentShield < game_message.constants.ship.maxShield * 0.4:
            for station in my_ship.stations.shields:
                if station.operator is None:
                    return False,  CrewMoveAction(crew.id, station.gridPosition)
        
        return True, None

    def get_crewmate_target_id_distance(self, crew: CrewMember, used_station_id: List[str]) -> CrewDistance:
        shields = list(filter(lambda crewDist: crewDist.stationId not in used_station_id, crew.distanceFromStations.shields))

        if len(shields) == 0:
            return None
        
        shields = sorted(shields, key = lambda r1: r1.distance)
        return shields[0]

