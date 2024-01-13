from typing import Dict, List, Tuple
from station_util import find_closest_crew_for_station, find_closest_station
from tasks.orient_ship_towards import OrientShipTowardsTask
from tasks.scan_radar import ScanRadarTask
from tasks.shield import ShieldTask
from tasks.shoot_n import ShootN

from tasks.task import Task
from game_message import GameMessage, Ship, Vector, TurretType
from world_info import get_euclidian_distance


# Brain logic
class GameModel:
    # ordered by priority
    queued_tasks: List[Tuple[Task]] = []
    known_ships_states: Dict[str, Tuple[int, Ship]] = {}
    target_ship_pos: Ship

    recon_expiry = 100

    def find_best_known_target(self) -> Ship:
        other_ships = [ship[1] for ship in self.known_ships_states.values() if ship[0] < self.recon_expiry]
        other_ships = sorted(other_ships, key = lambda s: s.currentShield + s.currentHealth)
        return other_ships[0]

    def find_closest_ship(self, our_ship: Ship, game_message: GameMessage) -> Vector:
        other_ships = [ship for team_id, ship in game_message.shipsPositions.items() if
                       team_id != game_message.currentTeamId]
        other_ships = sorted(other_ships, key=lambda s1: get_euclidian_distance(our_ship.worldPosition, s1))
        return other_ships[0]

    def get_shooter_count(self):
        shootTaskCount = 0
        for task in self.queued_tasks:
            if isinstance(task, ShootN):
                shootTaskCount += 1
        return shootTaskCount

    def queue_attacks(self, game_message: GameMessage):
        target_ship = None

        for ship in game_message.ships.values():
            if ship.worldPosition == self.target_ship_pos:
                target_ship = ship
                break

        if target_ship == None:
            self.queued_tasks.append(ShootN(self.target_ship_pos, 5,
                                            game_message.ships.get(game_message.currentTeamId).stations.turrets))
            return

        target_shield = target_ship.currentShield
        target_health = target_ship.currentHealth

        if (target_shield > game_message.constants.ship.maxShield * 0.2):
            self.queued_tasks.append(ShootN(target_ship.worldPosition, 10,
                                            game_message.ships.get(game_message.currentTeamId).stations.turrets, TurretType.EMP))
        else:
            self.queued_tasks.append(ShootN(target_ship.worldPosition, 5,
                                            game_message.ships.get(game_message.currentTeamId).stations.turrets))

    def __init__(self, game_message: GameMessage):
        our_ship = game_message.ships.get(game_message.currentTeamId)

        self.target_ship_pos = self.find_closest_ship(our_ship, game_message)
        self.queued_tasks.append(OrientShipTowardsTask(self.target_ship_pos))

        # for team_id in game_message.shipsPositions.keys():
        #     if team_id != game_message.currentTeamId:
        self.queued_tasks.append(ScanRadarTask(
            [team_id for team_id in game_message.shipsPositions.keys() if team_id != game_message.currentTeamId]))

        self.queue_attacks(game_message)

    #  Todo : add think logic here
    # Update tasks to do with priority
    # Call the dispatcher Update so that it chooses which crewmate to do a task
    def update(self, game_message: GameMessage):
        our_ship = game_message.ships.get(game_message.currentTeamId)

        # cleanup dead ships from state
        for ship in self.known_ships_states.values():
            if ship[1].teamId not in game_message.shipsPositions.keys():
                if ship[1].worldPosition == self.target_ship_pos:
                    self.target_ship_pos = None

                del self.known_ships_states[ship[1].teamId]

        # update known target with new info
        for ship in game_message.ships.values():
            if ship.teamId != game_message.currentTeamId:
                self.known_ships_states[ship.teamId] = (
                    game_message.currentTickNumber, ship)

        # if target is None find a new one
        if self.target_ship_pos == None:
            if len(self.known_ships_states) == 0:
                self.target_ship_pos = self.find_closest_ship(our_ship, game_message)
                self.queued_tasks.append(OrientShipTowardsTask(self.target_ship_pos))
            else:
                self.target_ship_pos = self.find_best_known_target().worldPosition
                self.queued_tasks.append(OrientShipTowardsTask(self.target_ship_pos))

        # rescan to refresh old data
        rescanIds = []
        for ship in self.known_ships_states.values():
            if game_message.currentTickNumber - ship[0] > self.recon_expiry:
                rescanIds.append(ship[1].teamId)

        if our_ship.currentShield < game_message.constants.ship.maxShield * 0.4:
            self.queued_tasks.append(ShieldTask())

        if len(rescanIds) != 0:
            self.queued_tasks.append(ScanRadarTask(rescanIds))

        while len(self.queued_tasks) < 4:
            self.queue_attacks(game_message)

        # figure out what should be done
        pass

    # return the N most important tasks
    def get_important_tasks(self, n: int) -> List[Tuple[Task]]:
        ret = self.queued_tasks[:n + 1]
        self.queued_tasks = self.queued_tasks[n + 1:]
        return ret
