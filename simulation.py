import matplotlib.pyplot as plt
import math # Using math.isclose for float comparison

def get_float_input(prompt):
    """Gets and validates float input from the user."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0 and prompt not in ["Force (N, negative for resistance): "]: # Allow negative force
                 print("Value cannot be negative (except for force). Please try again.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a number.")

def simulate_drag(
    initial_velocity,
    mass,
    drag_coefficient,
    cross_sectional_area,
    fluid_density,
    force_constant, # Added constant force input
    initial_position=0.0,
    time_step=0.01,
    max_time=100.0
):
    """
    Simulates the motion of an object with air resistance and a constant force.

    Args:
        initial_velocity (float): Starting velocity (m/s).
        mass (float): Mass of the object (kg).
        drag_coefficient (float): Drag coefficient (dimensionless).
        cross_sectional_area (float): Area facing the fluid (m^2).
        fluid_density (float): Density of the fluid (kg/m^3).
        force_constant (float): Additional constant force acting on the object (N).
                                Negative for opposing motion, positive for assisting.
        initial_position (float, optional): Starting position (m). Defaults to 0.0.
        time_step (float, optional): Simulation time step (s). Defaults to 0.01.
        max_time (float, optional): Maximum simulation time (s). Defaults to 100.0.

    Returns:
        tuple: (times, positions, velocities, drag_forces) - lists of data points.
    """
    # --- Input Validation ---
    if mass <= 0:
        raise ValueError("Mass must be positive.")
    if time_step <= 0:
        raise ValueError("Time step must be positive.")
    if cross_sectional_area < 0: # Allow zero area if drag is not considered
        raise ValueError("Cross-sectional area cannot be negative.")
    if drag_coefficient < 0: # Allow zero Cd if drag is not considered
        raise ValueError("Drag coefficient cannot be negative.")
    if fluid_density < 0: # Allow zero density if drag is not considered
        raise ValueError("Fluid density cannot be negative.")


    # --- Simulation Setup ---
    current_velocity = initial_velocity
    current_position = initial_position
    current_time = 0.0

    times = [current_time]
    positions = [current_position]
    velocities = [current_velocity]
    drag_forces = [] # Store drag force at each step

    # --- Simulation Loop (Discrete Steps) ---
    # Stop if velocity becomes zero/negative or max time is reached
    while current_velocity > 1e-6 and current_time < max_time:
        # 1. Calculate Drag Force for the *current* velocity
        #    Force opposes velocity, hence the sign depends on velocity direction.
        #    Assuming positive initial velocity means drag is negative.
        drag_force = 0.5 * fluid_density * drag_coefficient * (current_velocity**2) * cross_sectional_area
        drag_forces.append(drag_force) # Store the magnitude

        # 2. Calculate Net Force
        #    Drag always opposes motion. Constant force is as given.
        net_force = force_constant - drag_force if current_velocity > 0 else force_constant + drag_force

        # 3. Calculate Acceleration
        acceleration = net_force / mass

        # 4. Update Velocity (Euler method)
        next_velocity = current_velocity + acceleration * time_step

        # 5. Update Position (Euler method using *current* velocity)
        current_position = current_position + current_velocity * time_step

        # 6. Update Time
        current_time += time_step

        # 7. Store Results
        #    Prevent velocity becoming negative due to discrete step overshoot
        current_velocity = max(0, next_velocity)
        times.append(current_time)
        positions.append(current_position)
        velocities.append(current_velocity)

    # Add one last drag force calculation if the loop terminated
    if velocities:
        last_drag = 0.5 * fluid_density * drag_coefficient * (velocities[-1]**2) * cross_sectional_area
        drag_forces.append(last_drag)
        # Pad drag_forces if it's shorter than velocities (e.g., started at v=0)
        while len(drag_forces) < len(velocities):
             drag_forces.append(0) # Or handle appropriately if needed


    print(f"\nSimulation finished at time {current_time:.2f}s")
    if current_velocity <= 1e-6:
        print(f"Object stopped (velocity ~ 0 m/s).")
    elif current_time >= max_time:
        print(f"Maximum simulation time ({max_time}s) reached.")

    return times, positions, velocities, drag_forces

def plot_results(times, positions, velocities):
    """Plots and saves the simulation results."""
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:red'
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Velocity (m/s)', color=color)
    ax1.plot(times, velocities, color=color, label='Velocity')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('Position (m)', color=color)
    ax2.plot(times, positions, color=color, label='Position')
    ax2.tick_params(axis='y', labelcolor=color)

    fig.suptitle('Object Motion with Air Resistance and Constant Force')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    # Add legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc='center right')

    # Save the plot
    plt.savefig('motion_simulation_plot.png')
    print("\nPlot saved as 'motion_simulation_plot.png'")
    plt.show()

# --- Main Execution ---
if __name__ == "__main__":
    print("--- Air Resistance Simulation ---")

    # Get inputs from user
    v0 = get_float_input("Initial Velocity (m/s): ")
    m = get_float_input("Mass (kg): ")
    cd = get_float_input("Drag Coefficient (e.g., 1.05 for cube): ")
    area = get_float_input("Cross-sectional Area (m^2): ")
    rho = get_float_input("Fluid Density (kg/m^3, air≈1.225): ")
    f_const = get_float_input("Constant Force (N, negative for resistance): ")
    dt = get_float_input("Time Step (s, smaller is more accurate, e.g., 0.01): ")
    t_max = get_float_input("Maximum Simulation Time (s): ")

    # Run simulation
    try:
        t_data, x_data, v_data, drag_data = simulate_drag(
            initial_velocity=v0,
            mass=m,
            drag_coefficient=cd,
            cross_sectional_area=area,
            fluid_density=rho,
            force_constant=f_const,
            time_step=dt,
            max_time=t_max
        )

        # Print final air resistance if object stopped or simulation ended
        if v_data:
             final_velocity = v_data[-1]
             final_drag = 0.5 * rho * cd * (final_velocity**2) * area
             print(f"Final Velocity: {final_velocity:.4f} m/s")
             print(f"Final Drag Force: {final_drag:.4f} N")
        else:
             print("Simulation did not produce data points.")


        # Plot results
        if t_data: # Check if there's data to plot
             plot_results(t_data, x_data, v_data)
        else:
             print("No data to plot.")

    except ValueError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")