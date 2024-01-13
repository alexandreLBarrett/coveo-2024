from typing import Tuple
from ai_crewmate import *

class CrewmateDispatcher:
    crewmates: Dict[str, Crewmate] = {}

    def __init__(self, game_message: GameMessage):
        for crewmate in game_message.ships.get(game_message.currentTeamId).crew:
            self.crewmates[crewmate.id] = Crewmate(crewmate)

    def update_crewmates(self, game_message: GameMessage):
        for crewmate in game_message.ships.get(game_message.currentTeamId).crew:
            if crewmate.id not in self.crewmates:
                self.crewmates[crewmate.id] = Crewmate(crewmate)
            else:
                self.crewmates[crewmate.id].Update(crewmate)

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

    def update_tasks(self, newTasks: Tuple[Task, Task, Task, Task]):
        # TODO: implement
        pass
