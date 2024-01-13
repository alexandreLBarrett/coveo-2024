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
                crewmate = next([crew for crew in game_message.ships.get(game_message.currentTeamId).crew if crew.id == crewId])
                (is_done, action) = task.get_action(game_message, crewmate)
                actions.append(action)
                if is_done:
                    self.crewmates[crewId] = None

        return actions

    def get_available_crewmate_count(self) -> int:
        return len([task for task in self.crewmates.values() if task == None])

    def schedule_task(self, newTasks: List[Task]):
        # assign tasks to available and most adequate crewmate
        available_crewmates = [crew_str for crew_str in self.crewmates if self.crewmates.get(crew_str) is None]

        for j in range(len(available_crewmates)):
            min_task_dist: Tuple[int, Optional[Task]] = (int(math.inf), None)
            crew = find_crewmate_in_list(available_crewmates[j], game_message.ships[game_message.currentTeamId].crew)
            for i in range(len(newTasks)):
                (target_distance, target_station_index) = newTasks[i].get_crewmate_target_id_distance(crew)
                if target_distance < min_task_dist[0]:
                    min_task_dist = (target_distance, newTasks[i])

            # TODO: setTaskStation
            self.crewmates[crew.id] = min_task_dist[1]
            newTasks.pop(newTasks.index(min_task_dist[1]))
