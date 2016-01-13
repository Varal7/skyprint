from point import *


class Parabole():
    def __init__(self):
        self.origin = Point()
        self.time_at_explosion = 0
        self.phi = 0
        self.theta = 0
        self.initial_velocity = 0

    def init_from_origin(self, origin, time, phi, theta, initial_velocity):
        self.origin = Point()
        self.time_at_explosion = 0
        self.phi = 0
        self.theta = 0
        self.initial_velocity = 0
        
    def compute_height_at_explosion_from_origin(self):
