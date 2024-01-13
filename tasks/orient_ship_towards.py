from game_message import CrewMember, GameMessage, Vector
from station_util import get_station_position
from tasks.task import Task
from actions import CrewMoveAction, ShipLookAtAction

class OrientShipTowardsTask(Task):
    target_position: Vector

    def __init__(self, target_position: Vector):
        self.target_position = target_position

    def get_action(self, game_message: GameMessage, crew: CrewMember):
        if crew.gridPosition == get_station_position(self.station_id):
            action = ShipLookAtAction()
            action.target = self.target_position
            return True, action
        
        if crew.destination == None:
            action = CrewMoveAction()
            action.crewMemberId = crew.id
            action.destination = get_station_position(self.station_id)
            return False, action
        
        return False, None