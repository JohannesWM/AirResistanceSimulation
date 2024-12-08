from copy import copy
import json
from textwrap import indent

# Starting Variables

velocity = 40.45 # m/s or 90.5 mph
initial_x = 0 # feet
initial_y = 0 # feet

tick_speed = .0001 # seconds

vel_equation = lambda t, v, drag: v - (drag/1542.21)*t
drag_equation = lambda v: 0.5 * 1.28 * 1.21 * v*v * (1.25 * 1.890)

"""
Create Timeline of Velocity and other relevant data based on starting variables
"""

# Create velocity per time timeline

vel_zero = False
iter_vel = copy(velocity)
time = 0
velocity_timeline = []
drag_timeline = []
while not vel_zero:
    if time > 8.27:
        vel_zero = True
    # calculate drag based on v
    drag = drag_equation(iter_vel)
    iter_vel = vel_equation(tick_speed, iter_vel, drag)
    time += tick_speed
    velocity_timeline.append(iter_vel)
    drag_timeline.append(drag)
    print(iter_vel)

with open('velocity.json', 'w') as f:
    json.dump(velocity_timeline, f, indent=4)

x_pos_timeline = []
x_current = copy(initial_x)
for vel in velocity_timeline:
    x_progress = vel*tick_speed
    x_current += x_progress
    x_pos_timeline.append(x_current)

with open('x_pos.json', 'w') as f:
    json.dump(x_pos_timeline, f, indent=4)

# Boat math
boat_pos_timeline = []
current_x = 20.423 # meters
boat_vel = 1.98
for i in range(len(x_pos_timeline)):
    boat_pos_timeline.append(current_x)
    current_x += boat_vel*tick_speed

with open('boat_pos.json', 'w') as f:
    json.dump(boat_pos_timeline, f, indent=4)




