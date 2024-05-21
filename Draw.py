from Ellipse import *
import pygame.gfxdraw
import time

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

WINDOW_FORMAT = (800, 600)

ORIGIN = (int(WINDOW_FORMAT[0] / 2), int(WINDOW_FORMAT[1] / 2))

time_cache = []
time_now = time_last = 0

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("Fun with Ellipses Test")
    window = pygame.display.set_mode(WINDOW_FORMAT)

    draw_loop = True

    centre = ORIGIN

    #ell = Ellipse(centre, 200, 100, theta=math.pi / 6)

    surface = pygame.Surface((320, 240))
    red = (180, 50, 50)
    size = (0, 0, 300, 200)

    ellipse = pygame.draw.ellipse(surface, red, size)

    surface2 = pygame.transform.rotate(surface, 45)

    while draw_loop:
        if time_cache:
            time_now = time.time()
            time_cache.append(time_now - time_last)
            time_last = time_now
        else:
            time_cache.append(0)
            time_last = time.time()

        # Draw Screen
        window.fill(COLOR_BLACK)

        window.blit(surface2, (100, 100))

        """for y in range(0, WINDOW_FORMAT[1]):
            for x in range(0, WINDOW_FORMAT[0]):
                if ell.is_on_line(x, y):
                    pygame.gfxdraw.pixel(window, x, y, COLOR_WHITE)"""

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

    print(time_cache)
