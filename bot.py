import csv
import json
from game_message import *
from actions import *
from crewmates_dispatch import *
import random


class Bot:
    target_team: str

    def __init__(self):
        print("Initializing your super mega duper bot")
        self.target_team = None

    def compare_ship_hps(ship1: Ship, ship2: Ship) -> bool:
        if ship1.currentShield == ship2.currentShield:
            return ship1.currentHealth == ship2.currentHealth
        return ship1.currentShield < ship2.currentShield

    # find ship if none targetted or current target doesn't exist anymore
    def find_best_target(self, game_message: GameMessage): 
        if self.target_team != None:
            if game_message.ships.get(self.target_team) != None:
                return

        other_ships = [ship for ship in game_message.ships.values() if ship.teamId != game_message.currentTeamId]

        if len(other_ships) == 0:
            return

        other_ships = sorted(other_ships, self.compare_ship_hps)

        self.target_team = other_ships[0]

        print("targetted known team's ship -> ", self.target_team)

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        actions = []

        self.find_best_target(game_message)

        team_id = game_message.currentTeamId
        my_ship = game_message.ships.get(team_id)
        other_ships_ids = [
            shipId for shipId in game_message.shipsPositions.keys() if shipId != team_id]

        crew_mate_shooter = CrewMateDispatch()
        action_goto_turrets = crew_mate_shooter.assign_crew_turret(game_message)

        actions += action_goto_turrets
        
        # Now crew members at stations should do something!
        operatedTurretStations = [
            station for station in my_ship.stations.turrets if station.operator is not None]
        for turret_station in operatedTurretStations:
            possible_actions = [
                # Charge the turret.
                TurretChargeAction(turret_station.id),
                # Aim the turret itself.
                TurretLookAtAction(turret_station.id,
                                   Vector(random.uniform(0, game_message.constants.world.width), random.uniform(
                                       0, game_message.constants.world.height))
                                   ),
                # Shoot!
                TurretShootAction(turret_station.id)
            ]

            actions.append(random.choice(possible_actions))

        operatedHelmStation = [station for station in my_ship.stations.helms if station.operator is not None]
        if operatedHelmStation:
            actions.append(ShipRotateAction(random.uniform(0, 360)))

        operatedRadarStation = [
            station for station in my_ship.stations.radars if station.operator is not None]
        for radar_station in operatedRadarStation:
            actions.append(RadarScanAction(radar_station.id,
                           random.choice(other_ships_ids)))

        # You can clearly do better than the random actions above! Have fun!
        return actions
