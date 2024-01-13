from typing import Tuple

from ai_crewmate import Task
from game_message import GameMessage


# Brain logic
class GameModel:
    tasks = []

    def __init__(self):
        pass

    #  Todo : add think logic here
    # Update tasks to do with priority
    # Call the dispatcher Update so that it chooses which crewmate to do a task
    def update(self, game_message: GameMessage):
        pass

    def get_tasks(self) -> Tuple[Task, Task, Task, Task]:
        pass
