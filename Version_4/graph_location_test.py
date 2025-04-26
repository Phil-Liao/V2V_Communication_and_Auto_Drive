import pygame

class Simulation:
    def __init__(self, width=800, height=400):
        pygame.init()
        self.WIDTH = width
        self.HEIGHT = height
        self.CAR_A_COLOR = (255, 0, 0)  # Red
        self.CAR_B_COLOR = (0, 0, 255)  # Blue
        self.PEDESTRIAN_COLOR = (255, 255, 0)  # Yellow
        self.TEXT_COLOR = (255, 255, 255)
        self.CAR_WIDTH = 120
        self.CAR_HEIGHT = 60

        # Initialize positions directly
        self.car_a_pos = (150, self.HEIGHT // 3 - self.CAR_HEIGHT // 2)
        self.car_b_pos = (400, self.HEIGHT // 2 - self.CAR_HEIGHT // 2)  # Lowered Car B
        self.pedestrian_pos = (650, self.HEIGHT // 2)

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Relative Position Simulation")
        self.font = pygame.font.Font(None, 24)

    def update_car_a_position(self, new_x, new_y):
        """
        Updates the position of Car A.
        """
        self.car_a_pos = (new_x, new_y)

    def update_car_b_position(self, new_x, new_y):
        """
        Updates the position of Car B.
        """
        self.car_b_pos = (new_x, new_y)

    def update_pedestrian_position(self, new_x, new_y):
        """
        Updates the position of the pedestrian.
        """
        self.pedestrian_pos = (new_x, new_y)

    def draw_ruler_grid(self):
        """
        Draws a ruler grid on the borders of the canvas.
        """
        # Draw horizontal ruler
        for x in range(0, self.WIDTH, 50):  # Every 50 pixels
            pygame.draw.line(self.screen, (250, 250, 250), (x, 0), (x, 10))  # Top border ticks

        # Draw vertical ruler
        for y in range(0, self.HEIGHT, 50):  # Every 50 pixels
            pygame.draw.line(self.screen, (250, 250, 250), (0, y), (10, y))  # Left border ticks

    def draw_objects(self):
        """
        Draws the cars, pedestrian, their labels, and the ruler grid on the screen.
        """
        self.screen.fill((169, 169, 169))  # Grey background
        self.draw_ruler_grid()  # Draw the ruler grid
        pygame.draw.rect(self.screen, self.CAR_A_COLOR, (*self.car_a_pos, self.CAR_WIDTH, self.CAR_HEIGHT))
        pygame.draw.rect(self.screen, self.CAR_B_COLOR, (*self.car_b_pos, self.CAR_WIDTH, self.CAR_HEIGHT))
        pygame.draw.circle(self.screen, self.PEDESTRIAN_COLOR, self.pedestrian_pos, 30)

        # Draw labels
        self.screen.blit(self.font.render("Car A", True, self.TEXT_COLOR), 
                         (self.car_a_pos[0] + self.CAR_WIDTH // 2 - 25, self.car_a_pos[1] + 20))
        self.screen.blit(self.font.render("Car B", True, self.TEXT_COLOR), 
                         (self.car_b_pos[0] + self.CAR_WIDTH // 2 - 25, self.car_b_pos[1] + 20))
        self.screen.blit(self.font.render("Pedestrian", True, self.TEXT_COLOR), 
                         (self.pedestrian_pos[0] - 30, self.pedestrian_pos[1] - 60))

    def run(self):
        """
        Runs the main simulation loop.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_objects()
            pygame.display.flip()

        pygame.quit()

# Example usage
if __name__ == "__main__":
    sim = Simulation()

    # Demo: Reduced car movement with increased safe distance from Car B
    import threading
    import time
    import math

    def update_positions():
        car_a_speed = 1  # Reduced speed in pixels per frame
        car_b_speed = 1.5  # Reduced speed in pixels per frame
        car_a_direction = 1
        car_b_direction = -1
        safe_distance = sim.CAR_WIDTH + 50  # Minimum safe distance between cars
        pedestrian_safe_zone_a = 100  # Minimum distance from Car A
        pedestrian_safe_zone_b = 150  # Increased minimum distance from Car B

        while True:
            # Update Car A position
            new_car_a_x = sim.car_a_pos[0] + car_a_speed * car_a_direction
            if new_car_a_x < 0 or new_car_a_x + sim.CAR_WIDTH > sim.WIDTH:
                car_a_direction *= -1  # Reverse direction
            sim.update_car_a_position(new_car_a_x, sim.car_a_pos[1])

            # Update Car B position
            new_car_b_x = sim.car_b_pos[0] + car_b_speed * car_b_direction
            if new_car_b_x < 0 or new_car_b_x + sim.CAR_WIDTH > sim.WIDTH:
                car_b_direction *= -1  # Reverse direction
            sim.update_car_b_position(new_car_b_x, sim.car_b_pos[1])

            # Ensure safe distance between Car A and Car B
            if abs(sim.car_a_pos[0] - sim.car_b_pos[0]) < safe_distance:
                if sim.car_a_pos[0] < sim.car_b_pos[0]:
                    car_a_direction = -1
                    car_b_direction = 1
                else:
                    car_a_direction = 1
                    car_b_direction = -1

            # Ensure cars don't touch the pedestrian
            if abs(sim.car_a_pos[0] - sim.pedestrian_pos[0]) < pedestrian_safe_zone_a:
                car_a_direction *= -1
            if abs(sim.car_b_pos[0] - sim.pedestrian_pos[0]) < pedestrian_safe_zone_b:
                car_b_direction *= -1

            # Update Pedestrian position with a sinusoidal movement
            new_pedestrian_y = sim.HEIGHT // 2 + 50 * math.sin(time.time())
            if abs(sim.car_a_pos[0] - sim.pedestrian_pos[0]) >= pedestrian_safe_zone_a and \
               abs(sim.car_b_pos[0] - sim.pedestrian_pos[0]) >= pedestrian_safe_zone_b:
                sim.update_pedestrian_position(sim.pedestrian_pos[0], new_pedestrian_y)

            time.sleep(0.03)  # Control the update speed

    # Run the position updater in a separate thread
    threading.Thread(target=update_positions, daemon=True).start()

    sim.run()
