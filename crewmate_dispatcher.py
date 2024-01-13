from typing import Tuple
from tasks.task import *

class CrewmateDispatcher:
    crewmates: Dict[str, Task] = {}

    def __init__(self, game_message: GameMessage):
        for crew in game_message.ships.get(game_message.currentTeamId).crew:
            self.crewmates[crew.id] = None

    def get_stations_turrets(self, game_message: GameMessage) -> List[TurretStation]:
        team_id = game_message.currentTeamId
        my_ship = game_message.ships.get(team_id)

        return my_ship.stations.turrets

    def assign_crew_turret(self, game_message: GameMessage):
        actions = []

        team_id = game_message.currentTeamId
        my_ship = game_message.ships.get(team_id)

        turrets = self.get_stations_turrets(game_message)

        # tous les crew sauf le 0 qui est pilote
        for crewmate in my_ship.crew[1:]:
            if crewmate.currentStation is not turrets and crewmate.destination is None:
                visitable_stations_turrets = crewmate.distanceFromStations.turrets
                station_to_move_to = visitable_stations_turrets[0]
                actions.append(CrewMoveAction(
                    crewmate.id, station_to_move_to.stationPosition))

        return actions
    
    def get_actions(self, game_message: GameMessage):
        return [task.get_action(game_message) for task in self.crewmates.values() if task != None]
    
    def get_available_crewmate_count(self) -> int:
        return len([task for task in self.crewmates.values() if task == None])

    def schedule_task(self, newTasks: List[Task]):
        # assign tasks to available and most adequate crewmate
        pass
