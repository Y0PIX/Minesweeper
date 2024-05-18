import pygame
import random

def create_grid():
    temp_grid = []
    temp_grid_colors = []
    for row in range(rows):
        temp_grid.append([])
        temp_grid_colors.append([])
        for col in range(cols):
            temp_grid[row].append((pygame.Rect(tile_length * row + gap * row + margin_left, tile_length * col +
                                               gap * col + margin_top, tile_length, tile_length)))
            temp_grid_colors[row].append(unknown_color)
    return temp_grid, temp_grid_colors


def set_bombs():
    # set bombs
    temp_bomb_positions = []
    for i in range(bombs):
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        while (row, col) in temp_bomb_positions:
            row = random.randint(0, rows - 1)
            col = random.randint(0, cols - 1)
        temp_bomb_positions.append((row, col))
    return temp_bomb_positions


def game_loop():
    running = True
    game_over = False
    while running:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # TODO: move game over check if I implement a button for restart
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                for row in range(rows):
                    for col in range(cols):
                        # left-click to reveal unknown tiles
                        if (grid[row][col].collidepoint(event.pos) and grid_colors[row][col] == unknown_color and
                                event.button == 1):
                            if (row, col) in bomb_positions:
                                print("Game Over")
                                grid_colors[row][col] = bomb_color
                                game_over = True
                            else:
                                print("left-clicked on tile", row, col)
                                grid_colors[row][col] = known_color

                        # right-click to mark unknown tiles as bombs
                        elif (grid[row][col].collidepoint(event.pos) and grid_colors[row][col] == unknown_color and
                              event.button == 3):
                            print("right-clicked on tile", row, col)
                            grid_colors[row][col] = flag_color

                        # right-click again to unmark bombs
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


if __name__ == "__main__":
    # initialize pygame
    pygame.init()
    size = (width, height) = (1280, 720)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # changeable parameters
    gap = 2
    margin = 3 * gap
    tiles = (rows, cols) = (16, 12)
    bombs = 20
    unknown_color = "white"
    bomb_color = "orange"
    flag_color = "red"
    known_color = "black"

    # calculate tile size and margins
    play_size = play_size_width, play_size_height = (width - 2 * margin, height - 2 * margin)
    tile_length = min((play_size_width - gap * (rows - 1)) // rows, (play_size_height - gap * (rows - 1)) // cols)
    margin_left = margin + (play_size_width - (tile_length * rows + gap * (rows - 1))) // 2
    margin_top = margin + (play_size_height - (tile_length * cols + gap * (cols - 1))) // 2

    grid, grid_colors = create_grid()
    bomb_positions = set_bombs()
    game_loop()
    pygame.quit()
