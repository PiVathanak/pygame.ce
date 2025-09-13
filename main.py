# Circle moving with smooth wrap-around (Pac-Man style)
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
radius = 40  # circle radius
speed = 300  # pixels per second

while running:
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= speed * dt
    if keys[pygame.K_s]:
        player_pos.y += speed * dt
    if keys[pygame.K_a]:
        player_pos.x -= speed * dt
    if keys[pygame.K_d]:
        player_pos.x += speed * dt

    # wrap position (teleport logic for center point)
    if player_pos.x < 0:
        player_pos.x += screen.get_width()
    if player_pos.x > screen.get_width():
        player_pos.x -= screen.get_width()
    if player_pos.y < 0:
        player_pos.y += screen.get_height()
    if player_pos.y > screen.get_height():
        player_pos.y -= screen.get_height()

    # fill background
    screen.fill("purple")

    # draw circle with wrapping (extra copies on edges)
    for dx in (-screen.get_width(), 0, screen.get_width()):
        for dy in (-screen.get_height(), 0, screen.get_height()):
            pos = (player_pos.x + dx, player_pos.y + dy)
            pygame.draw.circle(screen, "red", pos, radius)

    # flip() the display
    pygame.display.flip()

    # limit FPS
    dt = clock.tick(60) / 1000

pygame.quit()
