# ngl idk python so there r a bunch of bugs but google is my bsf
import pygame as pg
import os
import random

TILE_SIZE = 48
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# basically maze so the 1s are the walls and the 0s are the walkable paths
MAZE = [
    "11111111110111111111",
    "10000001000001000001",
    "10111101011001011101",
    "10100001000101000001",
    "10101101011101101101",
    "10001000000001000101",
    "11101111101001101001",
    "10000001000101000001",
    "10110101110101011101",
    "10001000000100000001",
    "10101011110101111101",
    "10000000000000000001",
    "11111111111111111111"
]

def add_maze_border(maze):
    # what this does is add a solid border of the walls so the players doesnt go outta bounds
    wallrow = "1" * (len(maze[0]) + 2)
    bordered_maze = [wallrow]
    for row in maze:
        bordered_maze.append("1" + row + "1")
    bordered_maze.append(wallrow)
    return bordered_maze

MAZE = add_maze_border(MAZE)

MAZE_WIDTH = len(MAZE[0]) * TILE_SIZE
MAZE_HEIGHT = len(MAZE) * TILE_SIZE
MAZE_OFFSET_X = (SCREEN_WIDTH - MAZE_WIDTH) // 2
MAZE_OFFSET_Y = (SCREEN_HEIGHT - MAZE_HEIGHT) // 2

class Player(pg.sprite.Sprite):
    def __init__(self, pos):
        # intializes da player at a pixel, so its escaping from the cat
        # it also loads the player img and the speed it goes at, so 4
        super().__init__()
        image = pg.image.load("data/quokka1.png").convert_alpha()
        image = pg.transform.scale(image, (TILE_SIZE - 8, TILE_SIZE - 8))
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = 4

    def move(self, dx, dy, maze, offset):
        #moves player by dx and dy and checks colllisiosns with wall
        # returns true if move successfull ( so no collision) but if there is its false
        future_position = self.rect.move(dx, dy)
        col1 = (future_position.left - offset[0]) // TILE_SIZE
        row1 = (future_position.top - offset[1]) // TILE_SIZE
        col2 = (future_position.right - 1 - offset[0]) // TILE_SIZE
        row2 = (future_position.bottom - 1 - offset[1]) // TILE_SIZE

        if (
            0 <= row1 < len(maze) and
            0 <= col1 < len(maze[0]) and
            0 <= row2 < len(maze) and
            0 <= col2 < len(maze[0]) and
            all(maze[r][c] == "0" for r in (row1, row2) for c in (col1, col2))
        ):
            self.rect = future_position
            return True
        return False

class Cat(pg.sprite.Sprite):
    # INITIALIZES DA KITTY and so it spins
    def __init__(self, pos):
        super().__init__()
        image = pg.image.load("data/cat.png").convert_alpha()
        image = pg.transform.scale(image, (TILE_SIZE - 8, TILE_SIZE - 8))
        self.original_image = image
        self.image = image.copy()
        self.rect = self.image.get_rect(topleft=pos)
        self.pos = pos
        self.angle = 0
        self.spinning = True
        self.togglepoop = pg.time.get_ticks()
        self.pause_start = None

    def update(self):
        # updates whether the cat is spining or pausing
        now = pg.time.get_ticks()
        if self.spinning:
            self.angle += 5
            self.image = pg.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

            if now - self.togglepoop > random.randint(2000, 4000):
                self.spinning = False
                self.togglepoop = now
                self.pause_start = now
        else:
            if now - self.togglepoop > random.randint(2000, 4000):
                self.spinning = True
                self.toggle_time = now
                self.pause_start = None
            self.image = self.original_image
            self.rect.topleft = self.pos

class Leaf(pg.sprite.Sprite):
    # initializes leaf and how its placed randomly
    def __init__(self, maze, offset, occupied):
        super().__init__()
        image = pg.image.load("data/leaf.png").convert_alpha()
        self.image = pg.transform.scale(image, (TILE_SIZE - 12, TILE_SIZE - 12))
        self.maze = maze
        self.offset = offset
        self.occupied = occupied
        self.rect = self.image.get_rect()
        self.respawn()

    def respawn(self):
        # finding a diff posiiton without overlapping
        while True:
            row = random.randint(1, len(self.maze) - 2)
            col = random.randint(1, len(self.maze[0]) - 2)
            if self.maze[row][col] == "0":
                x = col * TILE_SIZE + self.offset[0]
                y = row * TILE_SIZE + self.offset[1]
                if not any(sprite.rect.collidepoint(x + TILE_SIZE//2, y + TILE_SIZE//2) for sprite in self.occupied):
                    self.rect.topleft = (x, y)
                    break

def main():
    pg.init()
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Maze Quest")
    clock = pg.time.Clock()

    background_tile = pg.image.load("data/realgrass.png").convert_alpha()
    floor_tile = pg.transform.scale(pg.image.load("data/sand.png").convert_alpha(), (TILE_SIZE, TILE_SIZE))

    player = None
    cat = None
    all_sprites = pg.sprite.Group()

    for y, row in enumerate(MAZE):
        for x, tile in enumerate(row):
            if tile == "0" and not player:
                pos = (x * TILE_SIZE + MAZE_OFFSET_X, y * TILE_SIZE + MAZE_OFFSET_Y)
                player = Player(pos)
                all_sprites.add(player)

    for x, tile in enumerate(MAZE[1]):
        if tile == "0":
            pos = (x * TILE_SIZE + MAZE_OFFSET_X, TILE_SIZE + MAZE_OFFSET_Y)
            cat = Cat(pos)
            all_sprites.add(cat)
            break

    leaf = Leaf(MAZE, (MAZE_OFFSET_X, MAZE_OFFSET_Y), [player])
    all_sprites.add(leaf)

    score = 0
    font = pg.font.Font(None, 36)
    big_font = pg.font.Font(None, 48)
    timer_start = pg.time.get_ticks()
    won = False
    game_over = False

    while True:
        dt = clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        keys = pg.key.get_pressed()
        dx = dy = 0
        if keys[pg.K_w]: dy = -player.speed
        if keys[pg.K_s]: dy = player.speed
        if keys[pg.K_a]: dx = -player.speed
        if keys[pg.K_d]: dx = player.speed

        now = pg.time.get_ticks()
        moved = dx != 0 or dy != 0

        if not (game_over or won):
            if cat:
                cat.update()
            if moved:
                player.move(dx, dy, MAZE, (MAZE_OFFSET_X, MAZE_OFFSET_Y))

            if cat and not cat.spinning:
                if cat.pause_start is None:
                    cat.pause_start = now
                if moved and now - cat.pause_start > 1000:
                    game_over = True

            if pg.sprite.collide_rect(player, leaf):
                score += 1
                leaf.respawn()

            if score >= 3:
                won = True

        for x in range(0, SCREEN_WIDTH, background_tile.get_width()):
            for y in range(0, SCREEN_HEIGHT, background_tile.get_height()):
                screen.blit(background_tile, (x, y))

        for y, row in enumerate(MAZE):
            for x, tile in enumerate(row):
                if tile == "0":
                    px = x * TILE_SIZE + MAZE_OFFSET_X
                    py = y * TILE_SIZE + MAZE_OFFSET_Y
                    screen.blit(floor_tile, (px, py))

        all_sprites.draw(screen)

        screen.blit(big_font.render("Level 1", True, (255, 255, 255)), (30, 20))

        time_1 = (pg.time.get_ticks() - timer_start) / 1000
        timer2 = big_font.render(f"{time_1:.2f}", True, (255, 255, 255))
        screen.blit(timer2, (30, 60))

        score_display = big_font.render(f"Leaves: {score}", True, (255, 255, 255))
        screen.blit(score_display, (30, 100))

        if won:
            message = big_font.render("You Win!", True, (10, 200, 10))
            screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, 10))
        elif game_over:
            message = big_font.render("Game Over!", True, (200, 10, 10))
            screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, 10))

        pg.display.flip()

    pg.quit()

if __name__ == "__main__":
    main()
# i got bored w the commemts js ask me heh
