import itertools
import math
from typing import Tuple

from station_util import find_crewmate_in_list
from tasks.task import *

class CrewmateDispatcher:
    crewmates: Dict[str, Optional[Task]] = {}

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
        actions = []
        for crewId, task in self.crewmates.items():
            if task is not None:
                crewmate = find_crewmate_in_list(crewId, game_message.ships.get(game_message.currentTeamId).crew)
                is_done, action = task.get_action(game_message, crewmate)
                if action != None:
                    actions.append(action)
                if is_done:
                    self.crewmates[crewId] = None

        return actions

    def get_available_crewmate_count(self) -> int:
        return len([task for task in self.crewmates.values() if task == None])

# We suppose the new tasks are in decreasing order of priority
    def schedule_task(self, newTasks: List[Task], game_message: GameMessage):
        # assign tasks to available and most adequate crewmate
        available_crewmates = [crew_str for crew_str in self.crewmates if self.crewmates.get(crew_str) is None]

        used_station_ids = [task.station_id for task in self.crewmates.values() if task != None]

        for j in range(len(available_crewmates)):
            if len(newTasks) == 0:
                break

            min_task_dist: Tuple[CrewDistance, Optional[Task]] = (None, None)
            crew = find_crewmate_in_list(available_crewmates[j], game_message.ships[game_message.currentTeamId].crew)
            for task in newTasks:
                crew_dist = task.get_crewmate_target_id_distance(crew, used_station_ids)
                if crew_dist != None and  crew_dist is not None and hasattr(crew_dist, 'distance'):
                    if crew_dist != None and (min_task_dist[0] == None or crew_dist.distance < min_task_dist[0].distance):
                        min_task_dist = (crew_dist, task)

            if (min_task_dist[0] == None or min_task_dist[1] == None):
                continue

            min_task_dist[1].set_station_id(min_task_dist[0].stationId)
            self.crewmates[crew.id] = min_task_dist[1]
            newTasks.pop(newTasks.index(min_task_dist[1]))
