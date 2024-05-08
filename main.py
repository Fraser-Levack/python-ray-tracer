import pygame
from renderer import Draw
import enviroment


def game_start():
    # Initialize Pygame
    pygame.init()

    # Set up the camera display
    width, height = 1000, 700
    win = pygame.display.set_mode((width, height))
    # Set up the title
    pygame.display.set_caption("Ray Renderer")
    # Set up the mini map
    mini_map = enviroment.Map(win)
    # get mini_map player object
    player = mini_map.player

    # Set up the clock
    clock = pygame.time.Clock()
    game_loop(clock, win, mini_map, player, width, height)


def game_loop(clock, win, mini_map, player, width, height):
    run = True
    while run:
        # Update the display

        # background colour
        win.fill((30, 30, 30))
        player.draw(win)
        # ray_angle = 180
        # ray_distance = 200
        # try:
        #     # check if rays is not empty
        #     if player.rays:
        #         ray_angle = player.rays[0].angle
        #         ray_distance = player.rays[0].length
        # except Exception as e:
        #     print(e)
        # print(Draw.calculate_x_from_angle(ray_angle, player.dir, player.fov, 1000, ray_distance))
        # step time in the environment

        # for each ray make a point on the screen
        points = [Draw.calculate_point_from_ray(ray, player.dir, player.fov, width) for ray in player.rays]
        # draw the points
        Draw.points(win, points)
        mini_map.step_time(player=player)
        run = mini_map.run
        # rays = player.get_rays()
        # for each_ray in rays:
            # each_ray.draw(win)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    game_start()
