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
        win.fill((10, 10, 10))
        #player.draw(win)
        lines = [Draw.calculate_line_from_ray(ray, player.dir, player.fov, width, height) for ray in player.rays]
        Draw.lines(win, lines)
        mini_map.step_time(player=player)
        run = mini_map.run

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    game_start()
