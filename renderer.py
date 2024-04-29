import pygame


class Draw:
    @staticmethod
    def point(win, x, y, color,):
        pygame.draw.circle(win, color, (x, y), 4)

    @staticmethod
    def points(win, points):
        for point in points:
            Draw.point(win, point[0], point[1], Draw.colour(point[2]))

    # method to calculate colour from a set distance
    # the closer the distance, the closer to red the colour
    @staticmethod
    def colour(distance):
        if distance < 0:
            distance = 0
        if distance > 255:
            distance = 255
        return 255, 255 - distance, 255 - distance

