import pygame


class Draw:
    @staticmethod
    def point(win, x, y, color,):
        pygame.draw.circle(win, color, (x, y), 4)

    @staticmethod
    def points(win, points):
        for point in points:
            # if point already has a colour set
            if len(point) == 3:
                Draw.point(win, point[0], point[1], point[2])
            else:
                colour = Draw.colour(point[2])
                Draw.point(win, point[0], point[1], colour)


    @staticmethod
    def line(win, start, end, color):
        pygame.draw.line(win, color, start, end, 2)

    @staticmethod
    def lines(win, lines):
        for line in lines:
            Draw.line(win, line[0], line[1], Draw.colour(line[2]))

    @staticmethod
    def calculate_x_from_angle(angle, player_dir, player_fov, width, distance):
        center_of_window = width // 2
        # calculate the angle from the player to the ray
        angle_from_player = angle - player_dir
        # adjust the x-coordinate based on the distance of the ray
        x = center_of_window + (angle_from_player * width) // (player_fov * distance) * 10
        return x

    @staticmethod
    def calculate_point_from_ray(ray, player_dir, player_fov, width):
        x = Draw.calculate_x_from_angle(ray.angle, player_dir, player_fov, width, ray.length)
        y = 450
        colour = Draw.ray_colour(ray)
        return x, y, colour

    # method to calculate colour from a set distance
    # the closer the distance, the closer to red the colour
    @staticmethod
    def colour(distance):
        if distance < 0:
            distance = 0
        if distance > 255:
            distance = 255
        return 255, 255 - distance, 255 - distance

    @staticmethod
    def ray_colour(ray):
        # change ray colour to black if greater than 200
        if ray.length > 200:
            return 0, 0, 0
        # make the ray more red based on length
        return 255, 255 - ray.length, 255 - ray.length

