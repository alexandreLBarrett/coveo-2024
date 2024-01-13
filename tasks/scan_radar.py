from typing import List

from game_message import CrewDistance, CrewMember, GameMessage
from station_util import get_station_position
from tasks.task import Task
from actions import CrewMoveAction, RadarScanAction

class ScanRadarTask(Task):
    target_team: List[str]

    def __init__(self, target_team : List[str]):
        self.target_team = target_team

    def get_action(self, game_message: GameMessage, crew: CrewMember):
        if crew.gridPosition == get_station_position(game_message, self.station_id):
            return (len(self.target_team) == 1), RadarScanAction(self.station_id, self.target_team.pop(0))
        
        if crew.destination == None:
            return False, CrewMoveAction(crew.id, get_station_position(game_message, self.station_id))
        
        return False, None
    
    def get_crewmate_target_id_distance(self, crew: CrewMember) -> CrewDistance:
        if len(crew.distanceFromStations.radars) == 0:
            return None

        radars = crew.distanceFromStations.radars
        radars = sorted(radars, key = lambda r1: r1.distance)
        return radars[0]

