# Physics Ball Simulator

## Try The game: [Physics Ball Simulator by dot-ammar](https://dot-ammar.itch.io/physics-ball-simulator)

## Overview

This game, designed in Python, is a physics-based simulation that provides an interactive and visual representation of key concepts from AP Physics 1. It allows users to control a ball's movement, observing real-time changes in velocity, acceleration, and distance traveled. The game's physics engine calculates the trajectory of the ball under the influence of gravity and user interactions, offering a practical understanding of kinematics and dynamics.

## Game Physics and Mathematics

### Gravity and Ball Movement

The Game simulates gravity and its effect on the ball's movement. Gravity is defined in terms of pixesl per frame squared, scaled to the screen's dimensions:

```python
PIXELS_PER_METER = 100
GRAVITY = 9.8 * PIXELS_PER_METER / (FPS**2)
```

### Ball Trajectory Prediction

The function `predict_path` calculates the ball's trajectory based on its current position, velocity, gravity, and screen boundaries. It uses a loop to iteratively update the ball's position using its velocity, adjusting for gravity with each step:

```python
for _ in range(max_steps):
    x += velocity_x
    y += velocity_y
    velocity_y += gravity
    path.append((x, y))
```

The program is written in a way that this is similar to:

```python
pos_x += vel_x * time_step
pos_y += vel_y * time_step + 0.5 * gravity * time_step ** 2
vel_y += gravity * time_step
```

$$
x = x_o + v_{xo}t+\frac12at^2
$$

$$
y = y_o + v_{yo}t+\frac12at^2
$$

$$
v_y = v_o + at
$$

### Collision Detection and Response

The game handles collisions with the ground, ceiling, and walls. Upon collision, it modifies the ball's velocity to simulate a bounce, applying a dampening factor to simulate energy loss:

```python
if ball_rect.bottom >= screen.get_height():
    ball_velocity[1] *= -0.7
    ball_velocity[0] *= friction
```

### Real-time Metrics Calculation

The game calculates and displays real-time metrics like velocity, acceleration, and distance traveled. Velocity and acceleration are computed in meters per second, considering the frame rate for time measurement. The distance is calculated by including the velocity over time:

```python
velocity_x = (ball_velocity[0] / PIXELS_PER_METER) * FPS
distance_traveled += velocity_magnitude * SECONDS_PER_FRAME
```

### Dragging and Throwing Mechanism

Users can interact with the ball, dragging and throwing it. The game tracks mouse movement to determine the ball's new velocity when released:

```python
if dragging:
    ball_velocity = weighted_velocity[:]
```

where `weighted_velocity` is defined by:

```python
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
```

This works to create a smooth throwing simulation.

## Relevance to AP Physics 1

The game demonstrates key concepts from the AP Physics 1 curriculum, including:

- Kinematics in one and two dimensions
- Newton's laws of motion
- Concepts of work, energy, and power
- Principles of linear momentum and collisions


https://github.com/dot-ammar/Physics_Ball_Simulator/assets/80134790/ef93fdf8-1283-44cc-8071-2ce82eb8996b

