from typing import List, Tuple

from tasks.task import Task
from game_message import GameMessage


# Brain logic
class GameModel:
    # ordered by priority
    queued_tasks: List[Tuple[float, Task]] = []

    def __init__(self):
        pass

    #  Todo : add think logic here
    # Update tasks to do with priority
    # Call the dispatcher Update so that it chooses which crewmate to do a task
    def update(self, game_message: GameMessage):
        # figure out what should be done
        pass

    def get_important_tasks(self, n: int) -> List[Task]:
        # return the N most important tasks        
        return self.queued_tasks[:n]
