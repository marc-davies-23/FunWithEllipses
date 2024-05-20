import math

from Ellipse import *
#import pygame
import pygame.gfxdraw

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

WINDOW_FORMAT = (800, 600)

ORIGIN = (int(WINDOW_FORMAT[0] / 2), int(WINDOW_FORMAT[1] / 2))

DELAY_10ms = 10  # 10 ms delay

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Fun with Ellipses Test")
    window = pygame.display.set_mode(WINDOW_FORMAT)

    draw_loop = True

    centre = ORIGIN

    ell = Ellipse(centre, 200, 100, theta=math.pi/6)

    while draw_loop:
        # Default delay; at 10ms, FPS ~ 100
        pygame.time.delay(DELAY_10ms)

        # Draw Screen
        window.fill(COLOR_BLACK)

        for y in range(0, WINDOW_FORMAT[1]):
            for x in range(0, WINDOW_FORMAT[0]):
                if ell.is_on_line(x, y):
                    pygame.gfxdraw.pixel(window, x, y, COLOR_WHITE)

        # End of Draw Screen
        pygame.display.update()

        # User Feedback
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    draw_loop = False
                    pygame.quit()
                case _:
                    pass
