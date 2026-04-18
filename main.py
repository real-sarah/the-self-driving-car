import pygame
from entities.car import Car
from engine.road import Road
from entities.npc_car import NPCCar
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

road = Road(800, 600, lane_count=3)
lane_index = 1   # middle lane
x = road.get_lane_center(lane_index)
car = Car(x, 500, road.lane_width)

# NPC cars

npc_cars = []

cars_per_lane = 5
spacing = 200

for lane in range(road.lane_count):
    x = road.get_lane_center(lane)

    for i in range(cars_per_lane):
        y = -i * spacing - random.randint(0, 100)

        npc_cars.append(
            NPCCar(x, y, road.lane_width, road, lane)
        )

camera_y = 0

running = True

while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    action = {
        "throttle" : 0,
        "steer" : 0,
    }

    if keys[pygame.K_UP] or keys[pygame.K_w]:
        action["throttle"] = 1
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        action["throttle"] = -1

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        action["steer"] = 1
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        action["steer"] = -1

    car.update(action, road)
    camera_y = int(car.y - 500)
    road.draw(screen, camera_y)

    for npc in npc_cars:
        npc.update(npc_cars)

        # if NPC goes too far below camera
        if npc.y - camera_y > 700:
            same_lane = [c for c in npc_cars if c.lane_index == npc.lane_index]

            min_y = min(c.y for c in same_lane)

            npc.y = min_y - random.randint(180, 300)
            npc.speed = random.uniform(1.2, 2.5)

        npc.draw(screen, camera_y)

    car.draw(screen, camera_y)

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
