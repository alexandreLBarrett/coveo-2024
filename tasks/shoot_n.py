from actions import *
from game_message import *
from station_util import *
from tasks.task import *


class ShootN(Task):
    def __init__(self, target_position: Vector, shoot_count: int, turrets: List[TurretStation],
                 weaponType: Optional[TurretType] = None):
        self.target_position = target_position
        self.turrets = turrets
        self.shoot_count = shoot_count
        self.weaponType = weaponType

    def get_action(self, game_message: GameMessage, crew: CrewMember):
        if crew.gridPosition == get_station_position(game_message, self.station_id):
            actions = []
            turret = get_turret_station(game_message, self.station_id)
            if game_message.constants.ship.stations.turretInfos.get(turret.turretType).rotatable:
                actions.append(TurretLookAtAction(stationId=self.station_id, target=self.target_position))

            if get_turret_station(game_message, self.station_id).charge < 0:
                return False, actions

            self.shoot_count -= 1
            actions.append(TurretShootAction(self.station_id))
            return self.shoot_count == 0, actions

        if crew.destination is None:
            return False, [CrewMoveAction(crew.id, get_station_position(game_message, self.station_id))]

        return False, None

    def get_crewmate_target_id_distance(self, crew: CrewMember, used_station_id: List[str]) -> CrewDistance:
        if self.weaponType is None:
            turrets = list(filter(lambda crewDist: crewDist.stationId not in used_station_id, crew.distanceFromStations.turrets))

            if len(turrets) == 0:
                return None
            
            turrets = sorted(turrets, key=lambda r1: r1.distance)
            return turrets[0]

        valid_weapon_turrets = []
        for i in range(len(self.turrets)):
            if self.turrets[i].turretType == self.weaponType and i < len(crew.distanceFromStations.turrets):
                valid_weapon_turrets.append(crew.distanceFromStations.turrets[i])

        valid_weapon_turrets = list(filter(lambda crewDist: crewDist.stationId not in used_station_id, valid_weapon_turrets))

        if len(valid_weapon_turrets) == 0:
            return None

        valid_weapon_turrets = sorted(valid_weapon_turrets, key=lambda r1: r1.distance)
        return valid_weapon_turrets[0]
