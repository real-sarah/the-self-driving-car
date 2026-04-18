import pygame


class Road:
    def __init__(self, width, height, lane_count = 3):
        """
        width, height is of the screen
        """

        self.width = width
        self.height = height
        self.lane_count = lane_count

        # total road width
        self.road_width = width * 0.8

        self.left = (width - self.road_width) / 2
        self.right = (width + self.road_width) / 2

        self.lane_width = self.road_width / lane_count


    def get_lane_center(self, lane_index):
        """
        returns the x coordinate of the lane center
        """
        # 0 to n - 1

        lane_index = max(0, min(lane_index, self.lane_count - 1))

        return self.left + self.lane_width * (lane_index + 0.5)

    def draw(self, screen, camera_y):

        # ==============================
        # 1. Draw road background
        # ==============================
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (self.left, 0, self.road_width, self.height)
        )

        # ==============================
        # 2. Draw lane dividers (dashed)
        # ==============================
        offset = int(camera_y % 40)

        for i in range(1, self.lane_count):
            x = self.left + i * self.lane_width

            # Use WORLD y positions
            start_y = int(camera_y // 40) * 40 - 40

            for y in range(start_y, int(camera_y + self.height), 40):
                screen_y = int(y - camera_y)

                pygame.draw.line(
                    screen,
                    (255, 255, 255),
                    (x, screen_y),
                    (x, screen_y + 20),
                    2
                )

        # ==============================
        # 3. Draw road borders (solid)
        # ==============================
        pygame.draw.line(screen, (255, 255, 255),
                         (self.left, 0), (self.left, self.height), 4)

        pygame.draw.line(screen, (255, 255, 255),
                         (self.right, 0), (self.right, self.height), 4)