import pygame
import random


def create_grid():
    """
        Create a grid for the Minesweeper game.

        Does not have any Args.

        Returns: 
            tuple: A tuple containing the grid, grid colors, and bomb count display.
    """
    temp_grid = []
    temp_grid_colors = []
    temp_show_bomb_count = []
    for row in range(rows):
        temp_grid.append([])
        temp_grid_colors.append([])
        temp_show_bomb_count.append([])
        for col in range(cols):
            temp_grid[row].append((pygame.Rect(tile_length * row + gap * row + margin_left, tile_length * col +
                                               gap * col + margin_top, tile_length, tile_length)))
            temp_grid_colors[row].append(unknown_color)
            temp_show_bomb_count[row].append(False)
    return temp_grid, temp_grid_colors, temp_show_bomb_count


def set_bombs():
    """
    Set bomb positions on the grid.

    Does not have any Args.

    Returns:
        set: A set of tuples representing bomb positions.
    """
    temp_bomb_positions = set()  # set to avoid duplicates in bomb positions
    while len(temp_bomb_positions) < bombs:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        temp_bomb_positions.add((row, col))
    return temp_bomb_positions


def count_bombs(row, col):
    """
    Count the number of bombs around a specific tile.

    Args:
        row (int): The row index of the tile.
        col (int): The column index of the tile.

    Returns:
        int: The number of bombs around the tile.
    """
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if ((0 <= row + i < rows) and (0 <= col + j < cols) and (i != 0 or j != 0) 
                    and (row + i, col + j) in bomb_positions):
                count += 1
    return count


def reveal_empty_tiles():
    """
    Reveal all empty tiles around the clicked tile. If an empty tile is found, add it to a list and repeat the process.

    Does not have any Args.

    Returns:
        None
    """
    global safe_tiles
    empty_tiles = []
    for row in range(rows):
        for col in range(cols):
            if grid_colors[row][col] == known_color and show_bomb_count[row][col] and count_bombs(row, col) == 0:
                empty_tiles.append((row, col))
    while empty_tiles:
        row, col = empty_tiles.pop()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if ((0 <= row + i < rows) and (0 <= col + j < cols) and (i != 0 or j != 0)
                        and grid_colors[row + i][col + j] == unknown_color):
                    grid_colors[row + i][col + j] = known_color
                    show_bomb_count[row + i][col + j] = True
                    safe_tiles -= 1
                    if count_bombs(row + i, col + j) == 0:
                        empty_tiles.append((row + i, col + j))


def change_clicked_tile(row, col, event, game_over):
    """
    Change the state of the clicked tile based on the mouse event.

    Args:
        row (int): The row index of the tile.
        col (int): The column index of the tile.
        event: The mouse event triggering the tile change.
        game_over (bool): Flag indicating if the game is over.

    Returns:
        bool: Flag indicating if the game is over after the tile change.
    """
    # left-click to reveal unknown tiles
    global safe_tiles
    if grid[row][col].collidepoint(event.pos):
        if grid_colors[row][col] == unknown_color and event.button == 1:
            # if bomb is clicked, reveal all bombs and end game
            if (row, col) in bomb_positions:
                print("You clicked on a bomb. Game Over!")
                for bomb_row, bomb_col in bomb_positions:
                    grid_colors[bomb_row][bomb_col] = bomb_color
                game_over = True
            # if no bombs are clicked, reveal number of bombs around the tile
            else:
                print("left-clicked on tile", row, col, "with", count_bombs(row, col), "bombs around")
                grid_colors[row][col] = known_color
                show_bomb_count[row][col] = True
                safe_tiles -= 1
                if count_bombs(row, col) == 0:
                    reveal_empty_tiles()

        elif grid_colors[row][col] == unknown_color and event.button == 3:
            print("right-clicked on tile", row, col)
            grid_colors[row][col] = flag_color

        elif grid_colors[row][col] == flag_color and event.button == 3:
            print("right-clicked on tile", row, col)
            grid_colors[row][col] = unknown_color
    return game_over


def draw_screen():
    """
    Draw the game screen with the grid and bomb count display.

    Does not have any Args.

    Returns:
        None
    """
    # fill the screen with a color to wipe away anything from last frame
    screen.fill((80, 80, 80))
    # draw the grid
    for row in range(rows):
        for col in range(cols):
            pygame.draw.rect(screen, grid_colors[row][col], grid[row][col])
            if show_bomb_count[row][col]:
                count = count_bombs(row, col)
                font = pygame.font.Font(None, tile_length * 2 // 3)
                text = font.render(str(count), True, (255, 255, 255))
                text_rect = text.get_rect(center=(grid[row][col].centerx, grid[row][col].centery))
                screen.blit(text, text_rect)
    if safe_tiles == 0:
        font = pygame.font.Font(None, 100)
        text = font.render("You Won! Press 'R' to play again!", True, (0, 0, 0), (255, 255, 255))
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)
    # update the screen
    pygame.display.flip()


def restart_game():
    """
    Restart the Minesweeper game by resetting the grid, grid colors, bomb count display, and bomb positions.

    Does not have any Args.

    Returns:
        None
    """
    global grid, grid_colors, show_bomb_count, bomb_positions, safe_tiles
    grid, grid_colors, show_bomb_count = create_grid()
    bomb_positions = set_bombs()
    safe_tiles = rows * cols - bombs
    game_loop()


def game_loop():
    """
    Main game loop for the Minesweeper game. Handles game events, player interactions, and screen updates.

    Does not have any Args.

    Returns:
        None
    """
    running = True
    game_over = False
    while running:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                print("Restarting game")
                restart_game()
                return
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                for row in range(rows):
                    for col in range(cols):
                        game_over = change_clicked_tile(row=row, col=col, event=event, game_over=game_over)

        # draw the screen
        draw_screen()
        # limit the frame rate
        clock.tick(60)


if __name__ == "__main__":
    # initialize pygame
    pygame.init()
    size = (width, height) = (1280, 720)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    # changeable parameters
    gap = 5
    min_margin = 3 * gap
    tiles = (rows, cols) = (16, 12)
    bombs = 20
    safe_tiles = rows * cols - bombs
    unknown_color = "white"
    bomb_color = "orange"
    flag_color = "red"
    known_color = "black"

    # calculate tile size and margins
    play_size = play_size_width, play_size_height = (width - 2 * min_margin, height - 2 * min_margin)
    tile_length = min((play_size_width - gap * (rows - 1)) // rows, (play_size_height - gap * (rows - 1)) // cols)
    margin_left = min_margin + (play_size_width - (tile_length * rows + gap * (rows - 1))) // 2
    margin_top = min_margin + (play_size_height - (tile_length * cols + gap * (cols - 1))) // 2

    # create grid, set bombs and start game loop
    grid, grid_colors, show_bomb_count = create_grid()
    bomb_positions = set_bombs()
    game_loop()
    pygame.quit()
