import pygame
import math
import csv


class Map:
    def __init__(self):
        # start new pygame window instance
        pygame.init()
        # Set up the display
        self.width, self.height = 600, 600
        self.win = pygame.display.set_mode((self.width, self.height))
        # Set up the title
        pygame.display.set_caption("mini map")
        # Set up the clock
        self.clock = pygame.time.Clock()
        self.run = True
        player = PlayerCamera([300, 300], 0, 60)
        self.game_loop(player)

    def game_loop(self, player):
        key_pressed = None
        # place mouse in center of screen
        pygame.mouse.set_pos([self.width // 2, self.height // 2])
        mouse_pos = [self.width // 2, self.height // 2]
        while self.run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.KEYDOWN:
                    key_pressed = event.key
                if event.type == pygame.KEYUP:
                    key_pressed = None
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = list(event.pos)

            # Update the display
            pygame.display.update()
            # background colour
            self.win.fill((30, 30, 30))
            walls = self.make_map()
            # update & draw the player
            player.update(key_pressed, mouse_pos, walls)
            player.draw(self.win)

            self.clock.tick(60)
        pygame.quit()

    def make_map(self):
        walls = []
        with open('walls.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                start = [int(row[0]), int(row[1])]
                end = [int(row[2]), int(row[3])]
                thickness = int(row[4])
                wall = Wall(start, end, thickness)
                wall.draw(self.win)
                walls.append(wall)
        return walls


class PlayerCamera:
    def __init__(self, start_pos, start_dir, fov):
        self.pos = start_pos
        self.dir = start_dir
        self.move_dir = [1, 0]
        self.speed = 2
        self.fov = fov
        self.rays = []
        # give player a rect for collision detection
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 5, 5)

    # draw the player as arrow on map
    def draw(self, win):
        pygame.draw.circle(win, (255, 0, 0), self.pos, 5)
        vector_position = self.calculate_position_vector()[0]
        pygame.draw.line(win, (255, 0, 0), self.pos, vector_position, 2)
        for ray in self.rays:
            ray.draw(win)

    def calculate_position_vector(self):
        vector_position = []
        # calculate the angle of the player by dividing the width of the screen by 360
        angle = ((math.pi * 2) * self.dir) / 360
        # calculate the position of the vector by adding the position of the player to the direction of the player
        vector_position.append(self.pos[0] + math.cos(angle) * 20)
        vector_position.append(self.pos[1] + math.sin(angle) * 20)
        return vector_position, angle

    def movement_position(self, key_pressed=None):
        angle = self.calculate_position_vector()[1]
        angle_increment = [math.cos(angle), math.sin(angle)]
        new_pos = self.pos[:]
        # base of off player wasd movement and player direction
        if key_pressed == pygame.K_w:
            new_pos[0] += angle_increment[0] * self.speed
            new_pos[1] += angle_increment[1] * self.speed

        if key_pressed == pygame.K_s:
            new_pos[0] -= angle_increment[0] * self.speed
            new_pos[1] -= angle_increment[1] * self.speed

        if key_pressed == pygame.K_a:
            new_pos[0] += angle_increment[1] * self.speed
            new_pos[1] -= angle_increment[0] * self.speed

        if key_pressed == pygame.K_d:
            new_pos[0] -= angle_increment[1] * self.speed
            new_pos[1] += angle_increment[0] * self.speed

        # returning new position
        return new_pos

    def collision_checker(self, new_pos, walls):
        # update the rect to the new position
        self.rect.topleft = new_pos
        # return false if no collision and true if collision
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                # if collision, return rect to old position
                self.rect.topleft = self.pos
                return True
        return False

    # change the direction of the player based on mouse movement
    def rotate(self, mouse_pos):
        self.dir = float(mouse_pos[0])

    # send out rays base of fov
    def send_rays(self, walls=None):
        self.rays = []
        for i in range(-self.fov // 2, self.fov // 2):
            self.rays.append(Ray(self.pos, self.dir + i))
        # cast rays
        for ray in self.rays:
            ray.cast(walls)

    def update(self, key_pressed, mouse_pos, walls):
        # get possible new position
        new_pos = self.movement_position(key_pressed)
        # check for collisions with walls from possible new position
        collision = self.collision_checker(new_pos, walls)
        # if no collision, update position and rect
        if not collision:
            self.pos = new_pos
            self.rect.topleft = new_pos
        self.rotate(mouse_pos)
        self.send_rays(walls)


class Ray:  # Ray class
    def __init__(self, start, angle):
        self.start = start
        self.angle = angle
        self.length = 200
        self.end = [self.start[0] + math.cos(math.radians(self.angle)) * 200,
                    self.start[1] + math.sin(math.radians(self.angle)) * 200]

    def draw(self, win):
        # update the end of the ray
        self.end = [self.start[0] + math.cos(math.radians(self.angle)) * self.length,
                    self.start[1] + math.sin(math.radians(self.angle)) * self.length]
        # change ray colour based on length if the ray is smaller make it more red
        # if no wall is hit, make it green
        if self.length < 200:
            pygame.draw.line(win, (255, 255 - self.length, 255 - self.length), self.start, self.end, 2)
        else:
            pygame.draw.line(win, (0, 255, 0), self.start, self.end, 2)

    # calculate the distance between the player and the wall the ray hits
    def distance(self, wall):
        x1, y1 = self.start
        x2, y2 = self.end
        x3, y3 = wall.start
        x4, y4 = wall.end

        # check if the lines are parallel
        if (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4) == 0:
            return None

        # calculate the point of intersection
        x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / (
                (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / (
                (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))

        # check if the point of intersection is on the line segments
        tolerance = 1e-5
        if x < min(x1, x2) - tolerance or x > max(x1, x2) + tolerance or x < min(x3, x4) - tolerance or x > max(x3,
                                                                                                                x4) + tolerance or \
                y < min(y1, y2) - tolerance or y > max(y1, y2) + tolerance or y < min(y3, y4) - tolerance or y > max(y3,
                                                                                                                     y4) + tolerance:
            return None

        return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)

    # check all walls for the closest wall
    # then use the distance method to calculate the distance an change length of ray
    def cast(self, walls):
        closest = None
        for wall in walls:
            dist = self.distance(wall)
            if dist is not None:
                if closest is None or dist < closest:
                    closest = dist
        if closest is not None:
            self.length = closest


class Wall:
    def __init__(self, start, end, thickness=10):
        self.start = start
        self.end = end
        self.thickness = thickness
        top_left = [min(start[0], end[0]), min(start[1], end[1])]
        bottom_right = [max(start[0], end[0]), max(start[1], end[1])]
        width = abs(bottom_right[0] - top_left[0]) + self.thickness
        height = abs(bottom_right[1] - top_left[1]) + self.thickness
        self.rect = pygame.Rect(top_left[0], top_left[1], width, height)

    def draw(self, win):
        pygame.draw.line(win, (255, 255, 255), self.start, self.end, self.thickness)


if __name__ == '__main__':
    test_map = Map()
