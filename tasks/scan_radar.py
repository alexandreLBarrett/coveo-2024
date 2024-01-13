from game_message import CrewMember, GameMessage
from station_util import get_station_position
from tasks.task import Task
from actions import CrewMoveAction, RadarScanAction

class ScanRadarTask(Task):
    target_team: str

    def __init__(self, target_team: str):
        self.target_team = target_team

    def get_action(self, game_message: GameMessage, crew: CrewMember):
        if crew.gridPosition == get_station_position(self.station_id):
            action = RadarScanAction()
            action.stationId = self.station_id
            action.targetShip = self.target_team
            return True, action
        
        if crew.destination == None:
            action = CrewMoveAction()
            action.crewMemberId = crew.id
            action.destination = get_station_position(self.station_id)
            return False, action
        
        return False, None