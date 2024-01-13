from game_message import *
from actions import *
import random


class CrewMateDispatch:
    def __init__(self):
        pass

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
                station_to_move_to = random.choice(visitable_stations_turrets)
                actions.append(CrewMoveAction(
                    crewmate.id, station_to_move_to.stationPosition))

        return actions
