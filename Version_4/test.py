import socket
import threading
import pygame
import math

pygame.init()

# Connection Data
host = '192.168.50.40'
port = 7777

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

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []
nicknames = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024).decode('ascii')
            print(str(message))
            broadcast(message.encode('ascii'))
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Visualization Function
def visualize():
    running = True
    car_a = None
    car_b = None
    pedestrian = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(white)

        # Draw objects based on received data
        for client in clients:
            try:
                message = client.recv(1024).decode('ascii')
                if message.startswith('A:'):
                    data = message[2:].strip('()').split(',')
                    car_b = (int(data[0])+car_a[0], int(data[1])+car_a[1], float(data[2])+car_a[2])
                elif message.startswith('B:'):
                    data = message[2:].strip('()').split(',')
                    pedestrian = (int(data[0])+car_b[0], int(data[1])+car_b[1], float(data[2])+car_b[2])
            except:
                continue
        car_a = (screen_width/10, screen_height/2, 0)
        # Draw Car A
        if car_a:
            draw_rotated_rectangle(screen, red, (car_a[0], car_a[1]), 50, 30, car_a[2], 'Car A')

        # Draw Car B
        if car_b:
            draw_rotated_rectangle(screen, green, (car_b[0], car_b[1]), 50, 30, car_b[2], 'Car B')

        # Draw Pedestrian
        if pedestrian:
            draw_circle(screen, blue, (pedestrian[0], pedestrian[1]), 20, 'Pedestrian')

        pygame.display.flip()

    pygame.quit()

# Start Server and Visualization
server_thread = threading.Thread(target=receive)
server_thread.start()

visualize()