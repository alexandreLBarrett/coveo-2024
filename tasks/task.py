from game_message import *
from actions import *

class Task:
    station_id: str

    def set_station_id(self, id: str):
        self.station_id = id

    def get_action(self, game_message: GameMessage, crew: CrewMember):
        pass