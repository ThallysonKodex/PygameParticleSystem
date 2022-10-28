import random

import pygame
import configparser as cp
from random import *

class Particles:
    def __init__(self, pos, config):
        self.cp = cp.ConfigParser()
        self.cp.read(config)

        self.position = pos
        self.particles = []



    def update_particles(self, screen, dt):
        for amnt in range(self.cp.getint("Attributes", "particle_population")):
            self.particles.append([[self.position[0], self.position[1]], [randint(-self.cp.getint("Direction", "vertical_length"), self.cp.getint("Direction", "vertical_length")) / 10 if self.cp.getboolean("Direction", "vertical_randomization") == True else 4,
                                                             randint(-self.cp.getint("Direction", "horizontal_length"), self.cp.getint("Direction", "horizontal_length")) / 10 if self.cp.getboolean("Direction", "horizontal_randomization") == True else 4], randint(self.cp.getint("Attributes", "initial_size") / 2, self.cp.getint("Attributes", "initial_size"))])

        self.color = [int(self.cp["Color"]["color_red"]), int(self.cp["Color"]["color_green"]), int(self.cp["Color"]["color_blue"])]
        for particle in self.particles:
            particle[0][0] += particle[1][0] * int(self.cp["Speed"]["movement_speed"]) * dt + int(self.cp["Direction"]["horizontal_amplitude"])

            if self.cp.getboolean("Direction", "vertical_inverse") is False:
                particle[0][1] -= particle[1][1] * int(self.cp["Speed"]["movement_speed"]) * dt + int(self.cp["Direction"]["vertical_amplitude"])
            else:
                particle[0][1] += particle[1][1] * int(self.cp["Speed"]["movement_speed"]) * dt + int(
                    self.cp["Direction"]["vertical_amplitude"])

            if self.cp.getboolean("Gravity", "inverse_gravity") is False:
                particle[1][1] -= 0.1 * int(self.cp["Speed"]["movement_speed"]) * dt
            else:
                particle[1][1] += 0.1 * int(self.cp["Speed"]["movement_speed"]) * dt
            particle[1][0] += 0.01 * int(self.cp["Speed"]["movement_speed"]) * dt
            particle[2] -= 0.01 * int(self.cp["Speed"]["movement_speed"]) * dt

            if particle[2] <= 0:
                self.particles.remove(particle)

            if self.cp["Attributes"]["shape"] == "circle":
                pygame.draw.circle(screen, self.color, particle[0], particle[2])
            elif self.cp["Attributes"]["shape"] == "square":
                pygame.draw.rect(screen, self.color, pygame.Rect(particle[0][0], particle[0][1], particle[2], particle[2]))
            elif self.cp["Attributes"]["shape"] == "custom":
                screen.blit(pygame.transform.scale(pygame.image.load(str(self.cp["Attributes"]["custom_file"])), (particle[2], particle[2])), pygame.Rect(particle[0][0], particle[0][1], 1, 1))



    def update_position(self, x=0, y=0):
        self.position[0] += x
        self.position[1] += y

