from game_message import CrewDistance, CrewMember, GameMessage, Vector
from station_util import get_station_position
from tasks.task import Task
from actions import CrewMoveAction, ShipLookAtAction

class OrientShipTowardsTask(Task):
    target_position: Vector

    def __init__(self, target_position: Vector):
        self.target_position = target_position

    def get_action(self, game_message: GameMessage, crew: CrewMember):
        if crew.gridPosition == get_station_position(game_message, self.station_id):
            return True, ShipLookAtAction(self.target_position)
        
        if crew.destination == None:
            return False, CrewMoveAction(crew.id, get_station_position(game_message, self.station_id))
        
        return False, None
    
    def get_crewmate_target_id_distance(self, crew: CrewMember) -> CrewDistance:
        if len(crew.distanceFromStations.helms) == 0:
            return None

        stations = crew.distanceFromStations.helms
        stations = sorted(stations, key = lambda r1: r1.distance)
        return stations[0]