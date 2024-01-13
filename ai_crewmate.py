import os
from game_message import *
from actions import *
from enum import Enum


class TaskType(Enum):
    NONE = 0
    TURRET = 1
    SHIELD = 2
    REPAIR = 3
    RADAR = 4


@dataclass
class Task:
    taskType = TaskType.NONE
    stationId = ""
    position = Vector(0, 0)


@dataclass
class Crewmate(CrewMember):
    task = Task

    def __init__(self, crewMember: CrewMember):
        self.id = crewMember.id
        self.currentStation = crewMember.currentStation
        self.destination = crewMember.destination
        self.distanceFromStations = crewMember.distanceFromStations

    def Update(self, crewMember: CrewMember):
        self.currentStation = crewMember.currentStation
        self.destination = crewMember.destination
        self.distanceFromStations = crewMember.distanceFromStations

    def UpdateTask(self, new_task: Task):
        self.task = new_task
