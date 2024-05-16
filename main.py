import pygame

# pygame setup
pygame.init()
size = width, height = (1280, 720)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running = True
tiles = rows, cols = (16, 12)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("lightgray")

    # RENDER YOUR GAME HERE
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(42 * row + 0.1 * width, 42 * col + 0.1 * height, 40, 40)
            pygame.draw.rect(screen, "white", rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
