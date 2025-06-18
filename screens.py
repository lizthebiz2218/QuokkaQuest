# surface fill visibility variables
TRANSPARENT = (0,0,0,0)
VISIBLE = (0,0,0,255)

# start button constants
START_WIDTH = 200
START_HEIGHT = 50
START_X, START_Y = ((SCREEN_WIDTH / 2) - (START_WIDTH / 2), (SCREEN_HEIGHT / 2) - (START_HEIGHT / 2))

# player constants
PLAYER_SPEED = 4

# methods for setting up non-player image graphics (screens and buttons)
# make buttons
def Buttonify(Picture, coords, surface, width, height, hide_condition):
    image = pg.transform.scale(pg.image.load(Picture).convert_alpha(), (width, height))
    imagerect = image.get_rect()
    imagerect.topright = coords
    surface.blit(image,imagerect)
    if hide_condition:
        image.fill(TRANSPARENT)
    else:
        image.fill(VISIBLE)
    return (image,imagerect)

# make screens
def Screenify(Picture, coords, surface, width, height, playing):
    image = pg.transform.scale(pg.image.load(Picture).convert_alpha(), (width, height))
    imagerect = image.get_rect()
    imagerect.topright = coords
    surface.blit(image,imagerect)
    if playing :
        image.fill(TRANSPARENT)
    else:
        image.fill(VISIBLE)

# main loop
    # around other booleans (won, game_over)
    is_playing = False

# start button and home screen
    home_screen = Screenify("Welcome to QuokkaQuesT.png", (0,0), screen, SCREEN_WIDTH, SCREEN_HEIGHT, is_playing)
    start_button = Buttonify("IMG_2983.png", (START_X, START_Y), screen, START_WIDTH, START_HEIGHT, is_playing)

    if event.type == pg.MOUSEBUTTONDOWN:
        mouse = pg.mouse.get_pos
        if start_button[1].collidepoint(mouse) :
           is_playing = True

    while is_playing :
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
        else :
            is_playing = False