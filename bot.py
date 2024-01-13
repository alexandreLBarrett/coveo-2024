import csv
import json
import os

from crewmate_dispatcher import CrewmateDispatcher
from game_model import GameModel
from game_message import *
from actions import *
from tasks.task import *
import random

class Bot:
    exportCSVData: bool = True
    target_team: str

    dispatcher: CrewmateDispatcher
    model: GameModel

    def __init__(self):
        print("Initializing your super mega duper bot")
        self.target_team = None
        self.recon_crew = None
        self.opponents_ships = {}
        self.dispatcher = None
        self.model = None

    def compare_ship_hps(ship1: Ship, ship2: Ship) -> bool:
        if ship1.currentShield == ship2.currentShield:
            return ship1.currentHealth == ship2.currentHealth
        return ship1.currentShield < ship2.currentShield

    # find ship if none targetted or current target doesn't exist anymore
   

    def get_next_move(self, game_message: GameMessage):
        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        if self.model == None:
            self.model = GameModel(game_message)

        if self.dispatcher == None:
            self.dispatcher = CrewmateDispatcher(game_message)

        self.model.update(game_message)
        self.dispatcher.schedule_task(self.model.get_important_tasks(self.dispatcher.get_available_crewmate_count()), game_message)
        return self.dispatcher.get_actions(game_message)

        actions = []

        for ship in game_message.ships.values():
            if ship.teamId != game_message.currentTeamId:
                self.opponents_ships[ship.teamId] = ship.teamId

        # if we have discovered all other ships
        if len(self.opponents_ships) == len(game_message.shipsPositions) - 1:
            self.find_best_target(game_message)

        team_id = game_message.currentTeamId
        my_ship = game_message.ships.get(team_id)
        other_ships_ids = [
            shipId for shipId in game_message.shipsPositions.keys() if shipId != team_id]

        crew_mate_shooter = CrewmateDispatcher(game_message)
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
