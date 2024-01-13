from cmath import sqrt
from game_message import Vector


def get_euclidian_distance(s1: Vector, s2: Vector):
    return sqrt(pow(s2.x - s1.x, 2) + pow(s2.y - s1.y, 2))