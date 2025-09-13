import pygame
import math

# --- Pac-Man Drawing Function ---
def draw_pacman(surface, pos, radius, mouth_angle=50, facing_angle=0, 
                color=(255, 255, 0), bg_color=(128, 0, 128)):
    """Draw a Pac-Man shape at pos with mouth facing facing_angle (in degrees)."""
    # Draw full circle
    pygame.draw.circle(surface, color, pos, radius)

    # Calculate mouth triangle points
    half_mouth = math.radians(mouth_angle / 2)
    angles = [facing_angle - half_mouth, facing_angle + half_mouth]

    points = [pos]  # center of pacman
    for angle in angles:
        x = pos[0] + radius * math.cos(angle)
        y = pos[1] + radius * math.sin(angle)
        points.append((x, y))

    # Cut mouth (draw background-colored triangle)
    pygame.draw.polygon(surface, bg_color, points)


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
    # Event handling
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

    # Normalize to keep diagonal speed consistent
    if move.length_squared() > 0:
        move = move.normalize()
        facing_angle = math.atan2(move.y, move.x)  # store direction
        player_pos += move * speed * dt

    # Clean wrap-around using modulo
    player_pos.x %= screen.get_width()
    player_pos.y %= screen.get_height()

    # Fill background
    screen.fill((128, 0, 128))  # purple

    # Draw Pac-Man and wrapped copies
    for dx in (-screen.get_width(), 0, screen.get_width()):
        for dy in (-screen.get_height(), 0, screen.get_height()):
            pos = (player_pos.x + dx, player_pos.y + dy)
            draw_pacman(screen, pos, radius, mouth_angle=50, facing_angle=facing_angle,
                        color=(255, 255, 0), bg_color=(128, 0, 128))

    # Flip display
    pygame.display.flip()

    # Cap dt to avoid big jumps
    dt = min(clock.tick(60) / 1000, 0.05)

pygame.quit()