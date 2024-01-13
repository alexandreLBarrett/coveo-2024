from game_message import CrewDistance, CrewMember, GameMessage
from station_util import get_station_position
from tasks.task import Task
from actions import CrewMoveAction, RadarScanAction

class ShieldTask(Task):
    target_team: str

    def __init__(self, target_team: str):
        self.target_team = target_team

    def get_action(self, game_message: GameMessage, crew: CrewMember):
        team_id = game_message.currentTeamId
        my_ship = game_message.ships.get(team_id)
        if my_ship.currentShield < game_message.constants.ship.maxShield * 0.4:
            for station in my_ship.stations.shields:
                if station.operator is None:
                    return False,  CrewMoveAction(crew.id, station.gridPosition)
        
        return True, None

