import pygame

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 400
ROAD_COLOR = (100, 100, 100)
CAR_A_COLOR = (255, 0, 0)  # Red
CAR_B_COLOR = (0, 0, 255)  # Blue
PEDESTRIAN_COLOR = (255, 255, 0)  # Yellow
TEXT_COLOR = (255, 255, 255)
LINE_COLOR = (255, 255, 0)  # Yellow
WHITE_LINE_COLOR = (255, 255, 255)  # White
GRASS_COLOR = (34, 139, 34)

# Object positions
CAR_WIDTH, CAR_HEIGHT = 120, 60
car_a_pos = (150, HEIGHT // (5.5/3))
car_b_pos = (400, HEIGHT // (4.05/3))
pedestrian_pos = (650, int(HEIGHT *10/11))

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Relative Position Simulation")

# Font setup
font = pygame.font.Font(None, 24)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background road
    screen.fill(ROAD_COLOR)
    
    # Draw double yellow lines
    line_y1 = HEIGHT // 2 - 10
    line_y2 = HEIGHT // 2 + 10
    pygame.draw.rect(screen, LINE_COLOR, (0, line_y1, WIDTH, 5))
    pygame.draw.rect(screen, LINE_COLOR, (0, line_y2, WIDTH, 5))
    
    # Draw white side lines
    white_line_y1 = HEIGHT * 0.25
    white_line_y2 = HEIGHT * 0.90  # Lowered for double lane effect
    pygame.draw.rect(screen, WHITE_LINE_COLOR, (0, white_line_y1, WIDTH, 5))
    pygame.draw.rect(screen, WHITE_LINE_COLOR, (0, white_line_y2, WIDTH, 5))
    
    # Draw green area above the top white line
    green_top_y1 = 0  # Starting at the top of the screen
    green_top_y2 = white_line_y1
    pygame.draw.rect(screen, GRASS_COLOR, (0, green_top_y1, WIDTH, green_top_y2))

    # Draw green area below the bottom white line
    green_bottom_y1 = white_line_y2
    green_bottom_y2 = HEIGHT
    pygame.draw.rect(screen, GRASS_COLOR, (0, green_bottom_y1, WIDTH, green_bottom_y2))


    # Draw dashed lane lines
    lane_y = (white_line_y2 + line_y2) / 2
    for x in range(0, WIDTH, 40):
        pygame.draw.rect(screen, WHITE_LINE_COLOR, (x, lane_y, 20, 5))

    # Draw cars and pedestrian
    pygame.draw.rect(screen, CAR_A_COLOR, (*car_a_pos, CAR_WIDTH, CAR_HEIGHT))
    pygame.draw.rect(screen, CAR_B_COLOR, (*car_b_pos, CAR_WIDTH, CAR_HEIGHT))
    pygame.draw.circle(screen, PEDESTRIAN_COLOR, pedestrian_pos, 30)

    # Draw labels
    # Draw labels above the objects
    screen.blit(font.render("Car A", True, TEXT_COLOR), (car_a_pos[0] + CAR_WIDTH // 2 - 25, car_a_pos[1] +20))
    screen.blit(font.render("Car B", True, TEXT_COLOR), (car_b_pos[0] + CAR_WIDTH // 2 - 25, car_b_pos[1] +20))
    screen.blit(font.render("Pedestrian", True, TEXT_COLOR), (pedestrian_pos[0] - 30, pedestrian_pos[1] - 60))

    # Update display
    pygame.display.flip()

pygame.quit()
