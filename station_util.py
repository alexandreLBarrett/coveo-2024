from actions import CrewMoveAction
from game_message import CrewDistance, CrewMember, Ship

def find_closest_station(crew_member: CrewMember, station_name: str) -> CrewDistance:
    stations: CrewDistance = crew_member.distanceFromStations[station_name]
    stations = sorted(stations, lambda r1, r2: r1.distance < r2.distance)
    return stations[0]

def compare_closest_to_station(crew1: CrewMember, crew2: CrewMember, station_name: str):
    distance1: CrewDistance = find_closest_station(crew1, station_name)
    distance2: CrewDistance = find_closest_station(crew2, station_name)
    return distance1.distance < distance2.distance

def find_crewmate_in_list(crewStr: str, crewList) -> CrewMember:
    return [crew for crew in crewList if crew.id == crewStr][0]

def move_crew_to_closest_station(self, crew: CrewMember, station_name: str) -> (CrewMoveAction, CrewDistance):
    closest_station = find_closest_station(crew, station_name)
    action = CrewMoveAction()
    action.crewMemberId = crew.id
    action.destination = closest_station.stationPosition
    return action, closest_station

def find_recon_crew(ship: Ship):
    idle_crewmates = [crewmate for crewmate in ship.crew if crewmate.currentStation is None and crewmate.destination is None]

    if len(idle_crewmates) == 0: 
        print("No crewmates available for recon")

    idle_crewmates = sorted(idle_crewmates, lambda c1, c2: compare_closest_to_station(c1, c2, "helm"))

    return idle_crewmates[0]