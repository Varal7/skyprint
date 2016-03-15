from point import *


class Parabole():
    def __init__(self, origin = Point(0,0), phi = 0, time = 0, theta = 0, initial_velocity = 0):
        self.origin = origin
        self.time_at_explosion = time
        self.phi = phi
        self.theta = theta
        self.initial_velocity = initial_velocity


    def compute_height_at_explosion_from_origin(self):
        
