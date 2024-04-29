import pygame
from renderer import Draw


def game_start():
    # Initialize Pygame
    pygame.init()

    # Set up the display
    width, height = 1000, 700
    win = pygame.display.set_mode((width, height))

    # Set up the title
    pygame.display.set_caption("Pygame Tutorial")

    # Set up the clock
    clock = pygame.time.Clock()
    game_loop(clock, win)


def game_loop(clock, win):
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update the display
        pygame.display.update()
        # background colour
        win.fill((30, 30, 30))
        points = [(100, 100, 200), (200, 200, 220), (300, 300, 100)]
        Draw.points(win, points)
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    game_start()
