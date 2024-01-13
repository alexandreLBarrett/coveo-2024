from typing import Dict, List, Tuple
from station_util import find_closest_crew_for_station, find_closest_station
from tasks.orient_ship_towards import OrientShipTowardsTask
from tasks.scan_radar import ScanRadarTask
from tasks.shoot_n import ShootN

from tasks.task import Task
from game_message import GameMessage, Ship, Vector
from world_info import get_euclidian_distance


# Brain logic
class GameModel:
    # ordered by priority
    queued_tasks: List[Tuple[Task]] = []
    known_ships_states: Dict[str, Tuple[int, Ship]] = {}

    def find_closest_ship(self, our_ship: Ship, game_message: GameMessage) -> Vector:
        other_ships = [ship for team_id, ship in game_message.shipsPositions.items() if team_id != game_message.currentTeamId]
        other_ships = sorted(other_ships, key = lambda s1: get_euclidian_distance(our_ship.worldPosition, s1))
        return other_ships[0]

    def __init__(self, game_message: GameMessage):
        our_ship = game_message.ships.get(game_message.currentTeamId)

        pos = self.find_closest_ship(our_ship, game_message)
        self.queued_tasks.append(OrientShipTowardsTask(pos))

        for team_id in game_message.shipsPositions.keys():
            if team_id != game_message.currentTeamId:
                self.queued_tasks.append(ScanRadarTask(team_id))

        self.queued_tasks.append(ShootN(-1, game_message.ships.get(game_message.currentTeamId).stations.turrets))
        self.queued_tasks.append(ShootN(-1, game_message.ships.get(game_message.currentTeamId).stations.turrets))

    #  Todo : add think logic here
    # Update tasks to do with priority
    # Call the dispatcher Update so that it chooses which crewmate to do a task
    def update(self, game_message: GameMessage):
        for ship in game_message.ships.values():
            if ship.teamId != game_message.currentTeamId:
                self.known_ships_states[ship.teamId] = (game_message.currentTickNumber, ship)

        for ship in self.known_ships_states.values():
            if ship[0] > 100:
                del self.known_ships_states[ship.teamId]
                
        # figure out what should be done
        pass

    # return the N most important tasks
    def get_important_tasks(self, n: int) -> List[Tuple[Task]]:
        ret = self.queued_tasks[:n+1]
        self.queued_tasks = self.queued_tasks[n+1:]
        return ret
