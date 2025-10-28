import pygame
import random
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Cool Circle Motion ✨")
clock = pygame.time.Clock()
running = True
dt = 0

# Player setup
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
player_speed = 400
player_radius = 30

# Particle system
particles = []

def draw_gradient_background(surface, color1, color2):
    """Draws a vertical gradient background."""
    for y in range(surface.get_height()):
        color = [
            color1[i] + (color2[i] - color1[i]) * (y / surface.get_height())
            for i in range(3)
        ]
        pygame.draw.line(surface, color, (0, y), (surface.get_width(), y))

def wrap_around(pos, width, height):
    """Makes the player wrap around screen edges."""
    if pos.x < 0: pos.x = width
    if pos.x > width: pos.x = 0
    if pos.y < 0: pos.y = height
    if pos.y > height: pos.y = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Create gradient background
    draw_gradient_background(screen, (255, 150, 200), (150, 200, 255))

    # Handle input
    keys = pygame.key.get_pressed()
    move = pygame.Vector2(0, 0)
    if keys[pygame.K_w]: move.y -= 1
    if keys[pygame.K_s]: move.y += 1
    if keys[pygame.K_a]: move.x -= 1
    if keys[pygame.K_d]: move.x += 1
    if move.length() > 0:
        move = move.normalize()
        player_pos += move * player_speed * dt

        # Add motion particles
        for _ in range(3):
            particles.append([
                [player_pos.x, player_pos.y],
                [random.uniform(-2, 2), random.uniform(-2, 2)],
                random.randint(3, 6)
            ])

    # Wrap around screen
    wrap_around(player_pos, screen.get_width(), screen.get_height())

    # Color-changing circle
    color_shift = (
        abs(int(math.sin(pygame.time.get_ticks() * 0.002) * 255)),
        abs(int(math.sin(pygame.time.get_ticks() * 0.003 + 2) * 255)),
        abs(int(math.sin(pygame.time.get_ticks() * 0.004 + 4) * 255)),
    )

    # Draw particles
    for particle in particles[:]:
        pos, vel, radius = particle
        pos[0] += vel[0]
        pos[1] += vel[1]
        radius -= 0.1
        pygame.draw.circle(screen, (255, 255, 255, 50), (int(pos[0]), int(pos[1])), int(radius))
        if radius <= 0:
            particles.remove(particle)

    # Draw player
    pygame.draw.circle(screen, color_shift, player_pos, player_radius)

    # Update display
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
