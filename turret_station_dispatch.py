import csv
import json
import os
from game_message import *
from actions import *
from crewmates_dispatch import *
import random


class TurretStationsDispatch:
    def __init__(self):
        pass

    def operate(self, game_message: GameMessage):
        actions = []

        team_id = game_message.currentTeamId
        my_ship = game_message.ships.get(team_id)

        # Now crew members at stations should do something!
        operatedTurretStations = [
            station for station in my_ship.stations.turrets if station.operator is not None]
        for turret_station in operatedTurretStations:
            if turret_station.charge < 0:
                action = TurretChargeAction(turret_station.id)
            else:
                action = TurretShootAction(turret_station.id)

            # possible_actions = [
            #     # Charge the turret.
            #     TurretChargeAction(turret_station.id),
            #     # Aim the turret itself.
            #     TurretLookAtAction(turret_station.id,
            #                        Vector(random.uniform(0, game_message.constants.world.width), random.uniform(
            #                            0, game_message.constants.world.height))
            #                        ),
            #     # Shoot!
            #     TurretShootAction(turret_station.id)
            # ]

            actions.append(action)

        return actions
