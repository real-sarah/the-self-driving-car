import math
import pygame
from entities.car import Car
import random

class NPCCar(Car):
    def __init__(self, x, y, lane_width, road, lane_index):
        super().__init__(x, y, lane_width)

        self.lane_index = lane_index
        self.road = road

        # NPCs move at constant speed
        self.base_speed = random.uniform(1.2, 2.5)
        self.speed = self.base_speed

    def draw(self, screen, camera_y):
        width = int(self.width)
        height = int(self.height)

        # Create surface
        car_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Draw NPC car (different color for clarity)
        pygame.draw.rect(car_surface, (0, 0, 255), (0, 0, width, height))

        # Rotate based on angle
        rotated = pygame.transform.rotate(car_surface, self.angle)

        # Convert world → screen coordinates
        screen_x = int(self.x)
        screen_y = int(self.y - camera_y)

        rect = rotated.get_rect(center=(screen_x, screen_y))

        screen.blit(rotated, rect.topleft)

    def update(self, npc_cars):
        rad = math.radians(self.angle)

        target_speed = self.base_speed

        closest = None
        min_dist = float("inf")

        for other in npc_cars:
            if other is self:
                continue

            if other.lane_index == self.lane_index:
                if other.y < self.y:  # ahead

                    dist = self.y - other.y

                    if dist < min_dist:
                        min_dist = dist
                        closest = other

        safe_distance = 200

        target_speed = self.base_speed

        if closest:
            if min_dist < safe_distance:
                # slow down proportionally
                factor = min_dist / safe_distance
                target_speed = closest.speed * factor


        # smooth speed change
        self.speed += (target_speed - self.speed) * 0.05
        if closest and min_dist < 40:
            self.speed = 0

        # lane centering
        lane_center = self.road.get_lane_center(self.lane_index)
        self.x += (lane_center - self.x) * 0.1

        # move forward
        self.x += self.speed * math.cos(rad)
        self.y -= self.speed * math.sin(rad)