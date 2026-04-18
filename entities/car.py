import pygame
import math

class Car:
    def __init__(self, x, y, lane_width):

        self.width = lane_width * 0.6
        self.height = self.width * 0.5

        # ==============================
        # POSITION
        # ==============================
        self.x = x
        self.y = y

        # ==============================
        # ORIENTATION
        # ==============================
        self.angle = 90  # car heading (degrees)

        # ==============================
        # MOTION
        # ==============================
        self.speed = 0

        # ==============================
        # CAR GEOMETRY
        # ==============================
        self.length = 40   # wheelbase (IMPORTANT for turning radius)

        # ==============================
        # PHYSICS LIMITS
        # ==============================
        self.max_speed = 6
        self.max_reverse = -2

        self.acceleration = 0.2
        self.brake_force = 0.4

        self.friction = 0.05

        # ==============================
        # STEERING
        # ==============================
        self.max_steering = 30  # max steering angle (degrees)
        self.steer_angle = 0    # current steering angle


        self.current_lane = 1 # start in the middle
        self.target_lane = 1 # start wanting to be in the middle

    def update(self, action, road=None):
        """
        action:
        {
            "throttle": -1 to 1,
            "steer": -1 to 1
        }

        road is optional (not used here yet)
        """

        # ==============================
        # 1. THROTTLE (ACCEL / BRAKE)
        # ==============================

        if action["throttle"] > 0:
            self.speed += self.acceleration

        elif action["throttle"] < 0:
            self.speed -= self.brake_force

        # ==============================
        # 2. FRICTION
        # ==============================

        if action["throttle"] == 0:
            if self.speed > 0:
                self.speed -= self.friction
                if self.speed < 0:
                    self.speed = 0

            elif self.speed < 0:
                self.speed += self.friction
                if self.speed > 0:
                    self.speed = 0

        # Kill tiny drift
        if abs(self.speed) < 0.01:
            self.speed = 0

        # ==============================
        # 3. CLAMP SPEED
        # ==============================

        self.speed = max(self.max_reverse, min(self.speed, self.max_speed))

        # ==============================
        # 4. STEERING (manual only)
        # ==============================

        target_steer = action["steer"] * self.max_steering

        # Smooth steering
        self.steer_angle += (target_steer - self.steer_angle) * 0.2

        # ==============================
        # 5. BICYCLE MODEL TURNING
        # ==============================

        if self.speed != 0:
            steer_rad = math.radians(self.steer_angle)

            angular_velocity = (self.speed / self.length) * math.tan(steer_rad)

            self.angle += math.degrees(angular_velocity)

        # ==============================
        # 6. MOVE CAR
        # ==============================

        rad = math.radians(self.angle)

        self.x += self.speed * math.cos(rad)
        self.y -= self.speed * math.sin(rad)


    def draw(self, screen, camera_y):

        width = int(self.width)
        height = int(self.height)

        car_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # body
        pygame.draw.rect(car_surface, (255, 0, 0), (0, 0, width, height))

        # front indicator (VERY useful visually)
        pygame.draw.rect(car_surface, (0, 255, 0), (width - 10, 5, 10, height - 10))

        rotated = pygame.transform.rotate(car_surface, self.angle)
        rect = rotated.get_rect(center=(int(self.x), 500))

        screen.blit(rotated, rect.topleft)