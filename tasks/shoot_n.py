from actions import *
from game_message import *
from station_util import *
from tasks.task import *

class ShootN(Task):
    def __init__(self, shoot_count: int, turrets: List[TurretStation], weaponType: Optional[TurretType] = None):
        self.turrets = turrets
        self.shoot_count = shoot_count
        self.weaponType = weaponType

    def get_action(self, game_message: GameMessage, crew: CrewMember):
        if crew.gridPosition == get_station_position(game_message, self.station_id):
            self.shoot_count -= 1
            return self.shoot_count == 0, TurretShootAction(self.station_id)

        if crew.destination is None:
            return False, CrewMoveAction(crew.id, get_station_position(game_message, self.station_id))

        return False, None

    def get_crewmate_target_id_distance(self, crew: CrewMember) -> CrewDistance:
        if self.weaponType is None:
            turrets = sorted(crew.distanceFromStations.turrets, key=lambda r1: r1.distance)
            return turrets[0]

        valid_weapon_turrets = []
        for i in range(len(self.turrets)):
            if self.turrets[i].turretType == self.weaponType:
                valid_weapon_turrets.append(crew.distanceFromStations.turrets[i])

        valid_weapon_turrets = sorted(valid_weapon_turrets, key=lambda r1: r1.distance)
        return valid_weapon_turrets[0]
