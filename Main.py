import tkinter as tk
from tkinter import messagebox, ttk
import random
import time
import threading

# Global variable to store simulation history
simulation_history = []

# Function to simulate sensor data collection
def simulate_sensor_data():
    """Simulate sensor readings for acceleration, gyroscope, GPS coordinates, and speed."""
    return (
        random.uniform(-10, 10),  # Acceleration in m/s^2
        random.uniform(-5, 5),    # Gyroscope value in degrees
        (random.uniform(-90, 90), random.uniform(-180, 180)),  # GPS coordinates
        random.uniform(0, 120)     # Speed in km/h
    )

# Function to check for crash detection
def check_for_crash(acceleration, gyroscope):
    """Check if the acceleration or gyroscope values exceed crash thresholds."""
    return abs(acceleration) > 5 or abs(gyroscope) > 3  # Thresholds for crash detection

# Function to update the data table and check for crashes
def update_data():
    """Run the simulation for 5 seconds, updating the data table and checking for crashes."""
    global simulation_history
    crash_detected = False
    start_time = time.time()

    while time.time() - start_time < 5:
        # Simulate sensor data
        acceleration, gyroscope, gps_coordinates, speed = simulate_sensor_data()
        crash_detected = check_for_crash(acceleration, gyroscope)

        # Log the data
        status = "Crashed" if crash_detected else "Not Crashed"
        log_entry = {
            "Time": time.strftime("%H:%M:%S"),
            "Speed": f"{speed:.2f} km/h",
            "Angle": f"{gyroscope:.2f}Â°",
            "Coordinates": f"{gps_coordinates}",
            "Status": status
        }
        simulation_history.append(log_entry)

        # Update the data table
        update_table(log_entry)

        # Delay for each simulated session
        time.sleep(0.5)
    
    # Show results after simulation
    messagebox.showinfo("Simulation Result", "Crash Detected! Emergency alert initiated." if crash_detected else "No Crash Detected.")

# Function to update the data table
def update_table(log_entry):
    """Update the data table with the latest log entry."""
    # Clear the current table
    for row in tree.get_children():
        tree.delete(row)

    # Insert the new log entry into the table
    tree.insert("", "end", values=(log_entry["Time"], log_entry["Speed"], log_entry["Angle"],
                                    log_entry["Coordinates"], log_entry["Status"]))

# Function to run the simulation in a separate thread
def run_simulation():
    """Start the simulation in a new thread to keep the UI responsive."""
    threading.Thread(target=update_data).start()

# Function to show simulation history
def show_history():
    """Display the history of simulation logs in a new window."""
    history_window = tk.Toplevel(root)
    history_window.title("Simulation History")

    # Create a text widget to display history
    history_text = tk.Text(history_window, width=80, height=20)
    history_text.pack()

    # Display each log entry
    for entry in simulation_history:
        history_text.insert(tk.END, f"Time: {entry['Time']}, Speed: {entry['Speed']}, "
                                     f"Angle: {entry['Angle']}, Coordinates: {entry['Coordinates']}, "
                                     f"Status: {entry['Status']}\n")

# Main menu interface
root = tk.Tk()
root.title("Smart Car Crash Detection System")

# Create a canvas for the car representation
canvas = tk.Canvas(root, width=400, height=300, bg="lightblue")
canvas.pack()

# Draw a simple representation of a car
canvas.create_rectangle(170, 130, 230, 170, fill="red")  # Car as a rectangle

# Create a frame for the data table
frame = tk.Frame(root)
frame.pack()

# Create a Treeview widget for the data table
tree = ttk.Treeview(frame, columns=("Time", "Speed", "Angle", "Coordinates", "Status"), show='headings')
for col in tree["columns"]:
    tree.heading(col, text=col)
tree.pack()

# Create buttons for starting the simulation and showing history
start_button = tk.Button(root, text="Start Simulation", command=run_simulation, width=30)
start_button.pack(pady=10)

history_button = tk.Button(root, text="Show History", command=show_history, width=30)
history_button.pack(pady=10)

# Start the Tkinter main loop
root.mainloop()
