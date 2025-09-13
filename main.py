import pygame
import math

# --- Pac-Man Drawing Function ---
def draw_pacman(surface, pos, radius, mouth_angle=50, facing_angle=0,
                color=(255, 255, 0), bg_color=(128, 0, 128)):
    """Draw a Pac-Man shape at pos with mouth facing facing_angle (radians)."""
    # Draw full circle
    pygame.draw.circle(surface, color, pos, radius)

    # Calculate mouth triangle points (slightly extend beyond radius to avoid leftover pixels)
    half_mouth = math.radians(mouth_angle / 2)
    angles = [facing_angle - half_mouth, facing_angle + half_mouth]

    points = [pos]  # center
    for angle in angles:
        x = pos[0] + (radius + 2) * math.cos(angle)  # radius+2 => fully cut
        y = pos[1] + (radius + 2) * math.sin(angle)
        points.append((x, y))

    pygame.draw.polygon(surface, bg_color, points)

    # --- Draw Eye ---
    # Eye position is rotated with Pac-Man direction
    eye_offset_angle = facing_angle - math.pi / 2  # eye slightly above mouth direction
    eye_distance = radius * 0.4  # distance from center
    eye_pos = (
        pos[0] + eye_distance * math.cos(eye_offset_angle),
        pos[1] + eye_distance * math.sin(eye_offset_angle)
    )
    pygame.draw.circle(surface, (0, 0, 0), eye_pos, radius * 0.12)  # small black eye


# --- Pygame Setup ---
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# --- Pac-Man Properties ---
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
radius = 40
speed = 300
facing_angle = 0  # radians, direction Pac-Man is facing

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    move = pygame.Vector2(0, 0)

    if keys[pygame.K_w]:
        move.y -= 1
    if keys[pygame.K_s]:
        move.y += 1
    if keys[pygame.K_a]:
        move.x -= 1
    if keys[pygame.K_d]:
        move.x += 1

    if move.length_squared() > 0:
        move = move.normalize()
        facing_angle = math.atan2(move.y, move.x)
        player_pos += move * speed * dt

    # Wrap-around using modulo
    player_pos.x %= screen.get_width()
    player_pos.y %= screen.get_height()

    # Draw background
    screen.fill((128, 0, 128))  # purple

    # Draw Pac-Man with wrap-around copies
    for dx in (-screen.get_width(), 0, screen.get_width()):
        for dy in (-screen.get_height(), 0, screen.get_height()):
            pos = (player_pos.x + dx, player_pos.y + dy)
            draw_pacman(screen, pos, radius, mouth_angle=50, facing_angle=facing_angle,
                        color=(255, 255, 0), bg_color=(128, 0, 128))

    pygame.display.flip()
    dt = min(clock.tick(60) / 1000, 0.05)

pygame.quit()
