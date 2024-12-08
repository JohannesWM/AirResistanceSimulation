from copy import copy
import json

tick_speed = 0.01 # seconds
velocity = 40.45 # m/s or 90.5 mph
initial_x = 0 # feet
initial_y = 0 # feet

vel_equation = lambda t, v: v - (9.81)*t

vel_zero = False
time = 0
iter_vel = copy(velocity)
velocity_timeline = []
while not vel_zero:
    if iter_vel <= -velocity:
        vel_zero = True
    # calculate drag based on v
    iter_vel = vel_equation(tick_speed, iter_vel)
    time += tick_speed
    velocity_timeline.append(iter_vel)

with open('velocity_y.json', 'w') as f:
    json.dump(velocity_timeline, f, indent=4)

y_pos_timeline = []
y_current = copy(initial_y)
for vel in velocity_timeline:
    y_progress = vel*tick_speed
    y_current += y_progress
    y_pos_timeline.append(y_current)

with open('y_pos.json', 'w') as f:
    json.dump(y_pos_timeline, f, indent=4)

# graph and save y-position over time

import matplotlib.pyplot as plt

# Generate a time vector for plotting
time_timeline = [tick_speed * i for i in range(len(y_pos_timeline))]

# Plot positions over time
plt.figure(figsize=(10, 6))
plt.plot(time_timeline, y_pos_timeline, label='Rectangle Position', color='blue')

# Add labels, legend, and title
plt.xlabel('Time (seconds)')
plt.ylabel('Position (meters)')
plt.title('Position of Rectangle and Boat Over Time')
plt.legend()
plt.grid()
plt.savefig("y_position_car.png", dpi=300)

# Show the plot
plt.show()