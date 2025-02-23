import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Object Locations")

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

# Font
font = pygame.font.Font(None, 36)

def draw_rotated_rectangle(surface, color, center, width, height, angle_degrees, label):
    """Draws a rotated rectangle on the surface with a label."""
    angle_radians = math.radians(angle_degrees)
    points = [
        (-width / 2, -height / 2),
        (width / 2, -height / 2),
        (width / 2, height / 2),
        (-width / 2, height / 2),
    ]

    rotated_points = []
    for x, y in points:
        new_x = x * math.cos(angle_radians) - y * math.sin(angle_radians)
        new_y = x * math.sin(angle_radians) + y * math.cos(angle_radians)
        rotated_points.append((new_x + center[0], new_y + center[1]))

    pygame.draw.polygon(surface, color, rotated_points)

    text = font.render(label, True, black)
    text_rect = text.get_rect(center=center)
    surface.blit(text, text_rect)

def draw_circle(surface, color, center, radius, label):
    """Draws a circle on the surface with a label."""
    pygame.draw.circle(surface, color, center, radius)

    text = font.render(label, True, black)
    text_rect = text.get_rect(center=center)
    surface.blit(text, text_rect)

def display_objects(object_data, labels):
    """Displays the objects based on the provided data with labels."""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(white)

        for i, obj in enumerate(object_data):
            x, y, angle = obj
            if labels[i] in ["A", "B"]:  # Draw rectangles for A and B
                width, height = 210, 140
                color = [red, green][i]
                draw_rotated_rectangle(screen, color, (x, y), width, height, angle, labels[i])
            else:  # Draw a circle for Pedestrian
                radius = 50
                draw_circle(screen, blue, (x, y), radius, labels[i])

        pygame.display.flip()

    pygame.quit()

# Example usage:
object_data = [
    [200, 300, 45],  # Object 1: x, y, angle
    [400, 200, 0],   # Object 2: x, y, angle
    [600, 400, 0],   # Object 3: x, y, angle (circle now)
]

labels = ["A", "B", "Pedestrian"]

display_objects(object_data, labels)