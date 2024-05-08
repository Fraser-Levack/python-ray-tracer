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
                try:
                    Draw.point(win, point[0], point[1], point[2])
                except Exception as e:
                    Draw.point(win, point[0], point[1], (20, 10, 10))
            else:
                colour = Draw.colour(point[2])
                Draw.point(win, point[0], point[1], colour)

    @staticmethod
    def line(win, start, end, color):
        try:
            pygame.draw.line(win, color, start, end, 8)
        except Exception as e:
            pygame.draw.line(win, (10, 10, 10), start, end, 8)

    @staticmethod
    def lines(win, lines):
        for line in lines:
            Draw.line(win, line[0], line[1], line[2])

    @staticmethod
    def calculate_x_from_angle(angle, player_dir, player_fov, width, distance):
        center_of_window = width // 2
        # calculate the angle from the player to the ray
        angle_from_player = angle - player_dir
        # adjust the x-coordinate based on the distance of the ray
        x = center_of_window + (angle_from_player * width) // player_fov // 1.5
        return x

    @staticmethod
    def calculate_point_from_ray(ray, player_dir, player_fov, width):
        x = Draw.calculate_x_from_angle(ray.angle, player_dir, player_fov, width, ray.length)
        y = 450
        colour = Draw.ray_colour(ray)
        return x, y, colour

    @staticmethod
    def calculate_line_from_ray(ray, player_dir, player_fov, width, height):
        x = Draw.calculate_x_from_angle(ray.angle, player_dir, player_fov, width, ray.length)
        # depending on the length of the ray, the y-coordinate will change
        # middle of line is in middle of screen
        y_middle = height // 2
        # if line is shorter the calculated line will be longer
        # calculate the top of the line
        y_top = y_middle + 400 - ray.length * 1.5
        # calculate the bottom of the line
        y_bottom = y_middle - 400 + ray.length * -1.5
        colour = Draw.ray_colour(ray)
        return (x, y_top), (x, y_bottom), colour

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
        if ray.length >= 200:
            return 10, 10, 10
        # make the ray closer to 30,30,30 the further away it is
        return 255 - ray.length, 255 - ray.length, 255 - ray.length

