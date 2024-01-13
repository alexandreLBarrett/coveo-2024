import abc

from game_message import *
from actions import *


class Task:
    station_id: str

    def set_station_id(self, station_id: str):
        self.station_id = station_id

    @abc.abstractmethod
    def get_action(self, game_message: GameMessage, crew: CrewMember):
        pass

    @abc.abstractmethod
    def get_crewmate_target_id_distance(self, crew: CrewMember) -> (int, str):
        # get all stations of target station type
        # get station closest to crew
        # return station position
        pass

    @abc.abstractmethod
    def get_station_type(self) -> str:
        pass
