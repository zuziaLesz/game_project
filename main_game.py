import pygame
from player import Player

TILE_SIZE = 40

pygame.init()
clock = pygame.time.Clock()
pygame.mixer.init()

display = pygame.display.set_mode((1000, 600))
pygame.display.set_caption('tree_grow')
font = pygame.font.SysFont(None, 36)

pygame.mixer.music.load("music.wav")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

pickup_sound = pygame.mixer.Sound("collect.wav")
portal_sound = pygame.mixer.Sound("portal.wav")
pickup_sound.set_volume(0.6)
portal_sound.set_volume(0.6)

background = pygame.image.load("background_trial.png").convert()

level_layout = [
    "0000000000000000000000000",
    "0000000000000000000000000",
    "00000000000000000000000X0",
    "00000000*0000PPPPPPPPPPP0",
    "0PPPpppPPPP00L00000000000",
    "000l000000l00L00000000000",
    "000l000000l00L00000000000",
    "0*0l000000l00L00000000000",
    "0PPP000000PPPP00000000000",
    "000L000000000000000000000",
    "000L000000000000000000000",
    "0@0L00000000000000000*000",
    "0PPPpppPPPPPPPPPPPpppPPP0",
    "0000000000000000000000000",
    "0000000000000000000000000"
]

level_two_layout = [
    "0000000000000000000000000",
    "0000000000000*00000000000",
    "000PPPPpppPPPPP0000000000",
    "000L0000000000L0000000000",
    "000L000*000000L0000000000",
    "000L00PPP00000L0X00000000",
    "000L00l0000000ppp00000000",
    "000L00l000000000000000000",
    "000L0*l000000000000000000",
    "000PPPP000000000000000000",
    "0000L00000000000000000000",
    "0@00L00000000000000000000",
    "0PPPP00000000000000000000",
    "0000000000000000000000000",
    "0000000000000000000000000"
]

pickups = []

pickup_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
pickup_img.fill((255, 255, 0))

platforms = []
ladders = []
hidden_platforms = []
hidden_ladders = []

player = Player(0, 0)
player_start = (0, 0)

platform_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
platform_img.fill((0, 100, 0))
ladder_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
ladder_img.fill((0, 100, 40))

portal_img = pygame.Surface((TILE_SIZE, TILE_SIZE))
portal_img.fill((255, 0, 0))

def draw_text_centered(text, size, color, y_offset=0):
    font_obj = pygame.font.SysFont(None, size)
    text_surf = font_obj.render(text, True, color)
    text_rect = text_surf.get_rect(center=(500, 300 + y_offset))
    display.blit(text_surf, text_rect)

def load_level(layout):
    global platforms, ladders, hidden_platforms, hidden_ladders, pickups, portal_rect, player, player_start

    platforms = []
    ladders = []
    hidden_platforms = []
    hidden_ladders = []
    pickups = []

    for y, row in enumerate(layout):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if tile == "P":
                platforms.append(rect)
            elif tile == "L":
                ladders.append(rect)
            elif tile == "p":
                hidden_platforms.append(rect)
            elif tile == "l":
                hidden_ladders.append(rect)
            elif tile == "*":
                pickups.append(rect)
            elif tile == "@":
                player = Player(x * TILE_SIZE, y * TILE_SIZE)
                player_start = (x * TILE_SIZE, y * TILE_SIZE)
            elif tile == "X":
                portal_rect = rect


load_level(level_layout)
runGame = True
show_hidden = False
collected_seeds = 0
revealed_tiles = []
game_state = "start"
attempts = 1
current_level_layout = level_layout

def reveal_closest_tiles(player, platforms, ladders, hidden_platforms, hidden_ladders, revealed_tiles, collected_seeds):
    for tile in revealed_tiles:
        if tile in platforms:
            platforms.remove(tile)
            hidden_platforms.append(tile)
        elif tile in ladders:
            ladders.remove(tile)
            hidden_ladders.append(tile)
    revealed_tiles.clear()

    def dist(r):
        return abs(player.rect.centerx - r.centerx) + abs(player.rect.centery - r.centery)

    closest_platform = min(hidden_platforms, key=dist, default=None)
    closest_ladder = min(hidden_ladders, key=dist, default=None)

    if closest_platform and (not closest_ladder or dist(closest_platform) <= dist(closest_ladder)):
        if collected_seeds >= 1 :
            to_reveal = sorted(hidden_platforms, key=dist)[:3]
            for tile in to_reveal:
                hidden_platforms.remove(tile)
                platforms.append(tile)
            revealed_tiles.extend(to_reveal)
    elif closest_ladder:
        if collected_seeds >= 2 :
            to_reveal = sorted(hidden_ladders, key=dist)[:3]
            for tile in to_reveal:
                hidden_ladders.remove(tile)
                ladders.append(tile)
            revealed_tiles.extend(to_reveal)
while runGame:

    display.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                runGame = False
            elif event.key == pygame.K_q:
                reveal_closest_tiles(player, platforms, ladders, hidden_platforms, hidden_ladders, revealed_tiles, collected_seeds)
            elif event.key == pygame.K_SPACE:
                if game_state == "start":
                    game_state = "instructions"
                elif game_state == "instructions":
                    game_state = "playing"
                elif game_state == "win":
                    load_level(level_layout)
                    current_level_layout = level_layout
                    collected_seeds = 0
                    revealed_tiles.clear()
                    attempts = 0
                    game_state = "playing"
    if game_state == "start":
        draw_text_centered("GAME NAME", 72, (255, 255, 255))
        draw_text_centered("Press SPACE to start", 36, (200, 200, 200), 60)

    elif game_state == "instructions":
        draw_text_centered("RULES:", 48, (255, 255, 255), -60)
        draw_text_centered("Collect pickups and press Q to reveal platforms and ladders.", 30, (255, 255, 255))
        draw_text_centered("You need one pickup to reveal platform and two for a ladder", 30, (255, 255, 255), 40)
        draw_text_centered("Reach the red portal with 3 pickups to proceed.", 30, (255, 255, 255), 80)
        draw_text_centered("Press SPACE to begin.", 30, (200, 200, 200), 120)

    elif game_state == "win":
        draw_text_centered("CONGRATULATIONS!", 64, (255, 255, 255), -60)
        draw_text_centered(f"Attempts: {attempts}", 36, (200, 200, 200), 0)
        draw_text_centered("Press SPACE to play again", 30, (180, 180, 180), 60)
        draw_text_centered("Press ESC to quit", 30, (180, 180, 180), 100)

    elif game_state == "playing":

        for rect in platforms:
            display.blit(platform_img, rect.topleft)

        for rect in ladders:
            display.blit(ladder_img, rect.topleft)

        keys = pygame.key.get_pressed()

        player.move(keys, platforms, ladders)
        player_rect = player.rect
        for pickup in pickups[:]:
            if player_rect.colliderect(pickup):
                pickups.remove(pickup)
                collected_seeds += 1
                pickup_sound.play()

        for pickup in pickups:
                display.blit(pickup_img, pickup.topleft)

        if portal_rect:
            display.blit(portal_img, portal_rect.topleft)
            if player.rect.colliderect(portal_rect) and collected_seeds >= 3:
                if level_layout == current_level_layout:
                    load_level(level_two_layout)
                    current_level_layout = level_two_layout
                    collected_seeds = 0
                    revealed_tiles.clear()
                    portal_sound.play()
                else:
                    game_state = "win"
        if (
                player.rect.top > 600 or
                player.rect.right < 0 or
                player.rect.left > 1000
        ):
            player.rect.topleft = player_start
            attempts += 1

        player.draw(display)
        seed_text = font.render(f"Seeds: {collected_seeds}", True, (255, 255, 255))
        text_rect = seed_text.get_rect(topright=(980, 10))
        display.blit(seed_text, text_rect)
        display.blit(portal_img, portal_rect.topleft)

    pygame.display.update()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
