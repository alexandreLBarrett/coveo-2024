from actions import CrewMoveAction
from game_message import CrewDistance, CrewMember, GameMessage, Ship, Vector

def find_closest_station(crew_member: CrewMember, station_name: str) -> CrewDistance:
    stations = crew_member.distanceFromStations[station_name]
    stations = sorted(stations, lambda r1: r1.distance)
    return stations[0]

def compare_closest_to_station(crew1: CrewMember, crew2: CrewMember, station_name: str):
    distance1: CrewDistance = find_closest_station(crew1, station_name)
    distance2: CrewDistance = find_closest_station(crew2, station_name)
    return distance1.distance < distance2.distance

def find_crewmate_in_list(crewStr: str, crewList) -> CrewMember:
    return [crew for crew in crewList if crew.id == crewStr][0]

def move_crew_to_closest_station(crew: CrewMember, station_name: str) -> (CrewMoveAction, CrewDistance):
    closest_station = find_closest_station(crew, station_name)
    action = CrewMoveAction()
    action.crewMemberId = crew.id
    action.destination = closest_station.stationPosition
    return action, closest_station

def find_closest_crew_for_station(ship: Ship, station_name: str):
    idle_crewmates = [crewmate for crewmate in ship.crew if crewmate.currentStation is None and crewmate.destination is None]

    if len(idle_crewmates) == 0: 
        print("No crewmates available for recon")
        return None

    idle_crewmates = sorted(idle_crewmates, key = lambda c1: find_closest_station(c1, station_name))

    return idle_crewmates[0]

def get_station_position(game_message: GameMessage, station_id: str) -> Vector:
    our_ship = game_message.ships.get(game_message.currentTeamId)

    stations = our_ship.stations.helms + our_ship.stations.radars + our_ship.stations.shields  + our_ship.stations.turrets
    
    return [station.gridPosition for station in stations if station.id == station_id][0]