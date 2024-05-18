import pygame
import random

# initialize pygame
pygame.init()
size = (width, height) = (1280, 720)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
running = True

# changeable parameters
gap = 2
tiles = (rows, cols) = (16, 12)
bombs = 20
unknown_color = "white"
bomb_color = "orange"
flag_color = "red"
known_color = "black"

# calculate tile size and margins
play_size = play_size_width, play_size_height = (width - 6 * gap, height - 6 * gap)
tile_length = min((play_size_width - gap * (rows - 1)) // rows, (play_size_height - gap * (rows - 1)) // cols)
margin_left = 3 * gap + (play_size_width - (tile_length * rows + gap * (rows - 1))) // 2
margin_top = 3 * gap + (play_size_height - (tile_length * cols + gap * (cols - 1))) // 2

# create a 2D list to store the grid
grid = []
grid_colors = []
for row in range(rows):
    grid.append([])
    grid_colors.append([])
    for col in range(cols):
        grid[row].append((pygame.Rect(tile_length * row + gap * row + margin_left, tile_length * col + gap * col +
                                      margin_top, tile_length, tile_length)))
        grid_colors[row].append(unknown_color)

# set bombs
bomb_positions = []
for i in range(bombs):
    row = random.randint(0, rows - 1)
    col = random.randint(0, cols - 1)
    while (row, col) in bomb_positions:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
    bomb_positions.append((row, col))

# game loop
while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for row in range(rows):
                for col in range(cols):
                    # left-click to change to known color
                    if (grid[row][col].collidepoint(event.pos) and grid_colors[row][col] == unknown_color and
                            event.button == 1):
                        print("left-clicked on tile", row, col)
                        grid_colors[row][col] = known_color

                    # right-click to change unknown color to red
                    elif (grid[row][col].collidepoint(event.pos) and grid_colors[row][col] == unknown_color and
                          event.button == 3):
                        print("right-clicked on tile", row, col)
                        grid_colors[row][col] = flag_color

                    # right-click again to change flag back to unknown
                    elif (grid[row][col].collidepoint(event.pos) and grid_colors[row][col] == flag_color and
                          event.button == 3):
                        print("right-clicked on tile", row, col)
                        grid_colors[row][col] = unknown_color

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((80, 80, 80))

    # draw the grid
    for row in range(rows):
        for col in range(cols):
            pygame.draw.rect(screen, grid_colors[row][col], grid[row][col])

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
