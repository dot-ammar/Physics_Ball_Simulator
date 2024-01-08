import pygame
import sys
import math


def predict_path(start_pos, start_velocity, gravity, screen_height, screen_width, max_steps=100):

    positions = []
    pos_x, pos_y = start_pos
    vel_x, vel_y = start_velocity

    for _ in range(max_steps):
        vel_y += gravity

        pos_x += vel_x
        pos_y += vel_y

        positions.append((pos_x, pos_y))

        if pos_y >= screen_height or pos_y <= 0 or pos_x >= screen_width or pos_x <= 0:
            break

    return positions

pygame.init()
pygame.font.init()

# Load font
font_path = 'OpenSans-Regular.ttf'
font_size = 24
custom_font = pygame.font.Font(font_path, font_size)

# Initialize metrics
distance_traveled = 0
start_time = pygame.time.get_ticks()

# Function to render text
def render_text(screen, text, pos, font=custom_font, color=(0, 0, 0)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

path = []  # List to store the ball's positions
path_length = 200  # Maximum length of the path

was_moving = False

height= 1000
width= 1000
screen = pygame.display.set_mode([height, width], pygame.RESIZABLE)

pygame.display.set_caption("Advanced Physics Ball")

ball_original = pygame.image.load("ball.png")  
ball_size = (50, 50)  
ball = pygame.transform.scale(ball_original, ball_size)
ball_rect = ball.get_rect(center=(250, 250))
ball_radius = ball_size[0] / 2

gravity = 0.5  # Gravity strength
friction = 0.98  # Friction coefficient on the ground
ball_velocity = [0, 0]  # Initial velocity of the ball
weighted_velocity = [0, 0]  # Weighted velocity for smooth throwing
alpha = 0.2  # Weight factor for averaging the velocity


dragging = False
last_mouse_pos = (0, 0)

clock = pygame.time.Clock()
FPS = 60

MIN_MOVEMENT_THRESHOLD = 5  

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.VIDEORESIZE:
            # Update the screen size
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            width, height = event.w, event.h  # Update width and height variables
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ball_rect.collidepoint(event.pos):
                dragging = True
                last_mouse_pos = event.pos
                ball_velocity = [0, 0]  # Reset velocity when picked up
                weighted_velocity = [0, 0]  # Reset weighted velocity
                start_time = 0  # Reset start time when ball is picked up
                distance_traveled = 0
                path.clear()
        

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                # Use the weighted velocity for the ball's velocity
                ball_velocity = weighted_velocity

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                current_mouse_pos = pygame.mouse.get_pos()
                ball_rect.center = current_mouse_pos
                
                # Calculate the instantaneous velocity
                movement_x = current_mouse_pos[0] - last_mouse_pos[0]
                movement_y = current_mouse_pos[1] - last_mouse_pos[1]

                if abs(movement_x) > MIN_MOVEMENT_THRESHOLD or abs(movement_y) > MIN_MOVEMENT_THRESHOLD:
                    instant_velocity = [movement_x, movement_y]

                    # Update the weighted velocity
                    weighted_velocity[0] = alpha * instant_velocity[0] + (1 - alpha) * weighted_velocity[0]
                    weighted_velocity[1] = alpha * instant_velocity[1] + (1 - alpha) * weighted_velocity[1]  

                else:
                    # Reset weighted_velocity if there's no significant movement
                    weighted_velocity = [0, 0]


                last_mouse_pos = current_mouse_pos


    if not dragging:
        # Apply gravity
        ball_velocity[1] += gravity
        ball_rect.x += ball_velocity[0]
        ball_rect.y += ball_velocity[1]
        
        # Collision with the ground
        if ball_rect.bottom >= screen.get_height():
            ball_rect.bottom = screen.get_height()
            ball_velocity[1] *= -0.7  
            ball_velocity[0] *= friction  

        # Collision with the top
        if ball_rect.top <= 0:
            ball_rect.top = 0
            ball_velocity[1] *= -0.7 

        # Collision with the walls
        if ball_rect.right >= screen.get_width() or ball_rect.left <= 0:
            ball_velocity[0] *= -0.7  
            if ball_rect.right >= screen.get_width():
                ball_rect.right = screen.get_width()
            elif ball_rect.left <= 0:
                ball_rect.left = 0
        
        # Add current position to the path
        path.append(ball_rect.center)
        if len(path) > path_length:
            path.pop(0)  # Remove the oldest point to maintain path length
        
        # Clear path on collision
        if ball_rect.bottom >= screen.get_height() or ball_rect.top <= 0 or \
           ball_rect.right >= screen.get_width() or ball_rect.left <= 0:
            distance_traveled = 0
            start_time = pygame.time.get_ticks()  # Reset start time on collision
            # path.clear()
    

    # Fill the background with white
    screen.fill((255, 255, 255))
    

    # Draw the predicted trajectory
    predicted_path = predict_path(ball_rect.center, ball_velocity, gravity, height, width)
    if len(predicted_path) > 1:
        for i in range(len(predicted_path) - 1):
            pygame.draw.line(screen, (255, 0, 0), predicted_path[i], predicted_path[i + 1], 2)  # Draw red lines
            
            
    # Draw the ball's trajectory
    if len(path) > 1:
        for i in range(len(path) - 1):
            pygame.draw.line(screen, (0, 0, 255), path[i], path[i + 1], 2)  # Draw blue lines

    # Calculate metrics
    if not dragging:
        current_time = (pygame.time.get_ticks() - start_time) / 1000  # Time in seconds
    else: 
        start_time = pygame.time.get_ticks()
        current_time = 0
        
    # Calculate X and Y velocities in meters/second
    velocity_x = ball_velocity[0] * FPS / 100  # Convert to meters/second
    velocity_y = ball_velocity[1] * FPS / 100  # Convert to meters/second

    # Update the overall velocity magnitude
    velocity_magnitude = math.sqrt(velocity_x**2 + velocity_y**2)

    # Update distance traveled in meters
    distance_traveled += velocity_magnitude * (1 / FPS)

    # Render metrics
    render_text(screen, f"Velocity: {velocity_magnitude:.2f} m/s", (10, 10))
    render_text(screen, f"Velocity X: {velocity_x:.2f} m/s", (10, 30))
    render_text(screen, f"Velocity Y: {velocity_y:.2f} m/s", (10, 50))
    render_text(screen, f"Distance: {distance_traveled:.2f} m", (10, 70))
    render_text(screen, f"Time: {current_time:.2f} s", (10, 90))

    # Draw the ball
    screen.blit(ball, ball_rect)

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

