import pygame
import sys
import math


def predict_path(start_pos, start_velocity, gravity, screen_height, screen_width, max_steps=10000):
    
    #print all the values of the perameters
    
    print("start_pos: ", start_pos)
    print("start_velocity: ", start_velocity)
    print("gravity: ", gravity)
    print("screen_height: ", screen_height)
    print("screen_width: ", screen_width)
    print("max_steps: ", max_steps)
    print("-----------------------------------")
    predicted_positions = []
    pos_x, pos_y = start_pos
    vel_x, vel_y = start_velocity
    time_step = 1 / FPS  

    for i in range(max_steps):
        pos_x += vel_x * time_step
        pos_y += vel_y * time_step + 0.5 * gravity * time_step**2
        vel_y += gravity * time_step

        # Check if the position is within screen bounds
        if 0 <= pos_x <= screen_width and 0 <= pos_y <= screen_height:
            predicted_positions.append((pos_x, pos_y))
        else:
            break
    return predicted_positions

def draw_pause_button(screen, hovered=False):
    
    button_color = pause_button_hover_color if hovered else pause_button_color
    pygame.draw.rect(screen, button_color, pause_button_rect)
    button_text_surface = custom_font.render(pause_button_text, True, pause_button_text_color)
    button_text_rect = button_text_surface.get_rect(center=pause_button_rect.center)
    screen.blit(button_text_surface, button_text_rect)

pygame.init()
pygame.font.init()

recalculate_path = True

MIN_VELOCITY_THRESHOLD = 0.1
# Button properties
pause_button_color = (200, 200, 200)  # Light gray
pause_button_hover_color = (170, 170, 170)  # Slightly darker gray
pause_button_text_color = (0, 0, 0)  # Black
pause_button_position = (10, 290)  # Top left, below your metrics
pause_button_size = (100, 40)  # Width, Height
pause_button_rect = pygame.Rect(pause_button_position, pause_button_size)
pause_button_text="Pause"
paused = False
button_hovered = False

# Load font
font_path = 'OpenSans-Regular.ttf'
font_size = 24
custom_font = pygame.font.Font(font_path, font_size)

frame = 0
# Initialize metrics
previous_velocity = 0
previous_velocity_x = 0
previous_velocity_y = 0
distance_traveled = 0
x_distance_traveled = 0
y_distance_traveled = 0 
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
ball_rect.center = (250,250)
FPS = 60

friction = 0.98  # Friction coefficient on the ground

PIXELS_PER_METER = 100  # 100 pixels = 1 meter
GRAVITY = 9.8 * PIXELS_PER_METER / (FPS**2)  # Gravity in pixels/frame^2

ball_mass = 1 

adjusted_gravity = GRAVITY * ball_mass

ball_velocity = [0, 0]  # Initial velocity of the ball
weighted_velocity = [0, 0]  # Weighted velocity for smooth throwing
alpha = 0.2  # Weight factor for averaging the velocity


ball_center_path = ball_rect.center
ball_velocity_path = [0,0]

dragging = False
last_mouse_pos = (0, 0)

clock = pygame.time.Clock()

MIN_MOVEMENT_THRESHOLD = 5

# Main game loop
while True:

    if paused:
        render_text(screen, f"X = x_o + Vx_o * t + 1/2 * a * t^2", (300, 50))
        render_text(screen, f"{x_distance_traveled:.2f} = 0 + Vx_o * {current_time:.2f} + 1/2 *  ", (300, 50))

        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == pygame.VIDEORESIZE:
            # Update the screen size
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            width, height = event.w, event.h  # Update width and height variables
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button_rect.collidepoint(mouse_pos):
                # Toggle the pause state
                paused = not paused
                pause_button_text = "Play" if paused else "Pause"
                draw_pause_button(screen, button_hovered)
            
            if ball_rect.collidepoint(event.pos) and not paused:
                dragging = True
                last_mouse_pos = event.pos
                ball_velocity = [0, 0]  # Reset velocity when picked up
                weighted_velocity = [0, 0]  # Reset weighted velocity
                start_time = 0  # Reset start time when ball is picked up
                distance_traveled = 0
                x_distance_traveled = 0
                y_distance_traveled = 0 
                path.clear()

        

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging and not paused:
                dragging = False

                print("ball_rect.center: ", ball_rect.center)
                print("ball_velocity: ", ball_velocity)
                
                ball_center_path = ball_rect.center[:]
                ball_velocity_path = ball_velocity[:]
                print("ball_velocity_path: ", ball_velocity_path)
                # Use the weighted velocity for the ball's velocity
                recalculate_path = True  # Set the flag here

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            if pause_button_rect.collidepoint(mouse_pos):
                # The mouse is over the button
                button_hovered = True
            else:
                button_hovered = False
    
            if dragging and not paused:
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
                    ball_velocity = weighted_velocity[:]  # Update the ball's velocity 
                else:
                    # Reset weighted_velocity if there's no significant movement
                    weighted_velocity = [0, 0]


                last_mouse_pos = current_mouse_pos
    if not paused:
        if not dragging:
            
            # Add current position to the path
            path.append(ball_rect.center)
            if len(path) > path_length:
                path.pop(0)  # Remove the oldest point to maintain path length
                
            # Apply gravity
            # Apply gravity (adjusted for scale and frame rate)
            ball_velocity[1] += adjusted_gravity
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
            
            
            # Clear path on collision
            if ball_rect.bottom >= screen.get_height() or ball_rect.top <= 0 or \
            ball_rect.right >= screen.get_width() or ball_rect.left <= 0:
                distance_traveled = 0
                x_distance_traveled = 0
                y_distance_traveled = 0 
                start_time = pygame.time.get_ticks()  # Reset start time on collision
                predicted_path.clear()
                # recalculate_path = True
                # path.clear()
                
        
    


    


    if not paused:
        
        
        # Fill the background with white
        screen.fill((255, 255, 255))
        
        
        # Draw the predicted trajectory
        if recalculate_path:
            print("ball_velocity_path: ", ball_velocity_path)
            predicted_path = predict_path(ball_center_path, ball_velocity_path, adjusted_gravity, height, width)
            recalculate_path = False
            
        if len(predicted_path) > 1:
            for i in range(len(predicted_path) - 1):
                pygame.draw.line(screen, (255, 0, 0), predicted_path[i], predicted_path[i + 1], 2)  # Draw red lines
                
                
        # Draw the ball's trajectory
        if len(path) > 1:
            for i in range(len(path) - 1):
                pygame.draw.line(screen, (0, 0, 255), path[i], path[i + 1], 2)  # Draw blue lines
                
        SECONDS_PER_FRAME = 1 / FPS  # Time per frame in seconds

        # Update the start time and current time
        if not dragging:
            current_time = (pygame.time.get_ticks() - start_time) / 1000  # Time in seconds
        else:
            start_time = pygame.time.get_ticks()
            current_time = 0

        # Convert velocities from pixels/frame to meters/second
        velocity_x = (ball_velocity[0] / PIXELS_PER_METER) * FPS  # meters/second
        velocity_y = (ball_velocity[1] / PIXELS_PER_METER) * FPS * -1  # meters/second

        # Update the overall velocity magnitude
        velocity_magnitude = math.sqrt(velocity_x**2 + velocity_y**2)

        # Update distance traveled in meters
        distance_traveled += velocity_magnitude * SECONDS_PER_FRAME
        x_distance_traveled += velocity_x * SECONDS_PER_FRAME
        y_distance_traveled += velocity_y * SECONDS_PER_FRAME



        acceleration_x = (velocity_x - previous_velocity_x) / SECONDS_PER_FRAME
        acceleration_y = (velocity_y - previous_velocity_y) / SECONDS_PER_FRAME
        acceleration = math.sqrt(acceleration_x**2 + acceleration_y**2)
        # Update previous velocities for the next frame
        previous_velocity = velocity_magnitude
        previous_velocity_x = velocity_x
        previous_velocity_y = velocity_y
        # Render metrics
        render_text(screen, f"Velocity: {velocity_magnitude:.2f} m/s", (10, 10))
        render_text(screen, f"Velocity X: {velocity_x:.2f} m/s", (10, 30))
        render_text(screen, f"Velocity Y: {velocity_y:.2f} m/s", (10, 50))
        
        render_text(screen, f"Acceleration: {acceleration:.2f} m", (10, 90))
        render_text(screen, f"Acceleration X: {acceleration_x:.2f} m", (10, 110))
        render_text(screen, f"Acceleration Y: {acceleration_y:.2f} m", (10, 130))
        
        render_text(screen, f"Distance: {distance_traveled:.2f} m", (10, 170))
        render_text(screen, f"X Distance: {x_distance_traveled:.2f} m", (10, 190))
        render_text(screen, f"Y Distance: {y_distance_traveled:.2f} m", (10, 210))
        render_text(screen, f"Time: {current_time:.2f} s", (10, 250))
        # Draw the ball
        screen.blit(ball, ball_rect)

    draw_pause_button(screen, button_hovered)



    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

