import json
from tkinter import Tk, Label, Frame

# Define fields based on indices
FIELD1_INDICES = {0, 1, 2, 3, 8, 10}  # Field1: Wheat
FIELD2_INDICES = {4, 5, 6, 7, 9, 11}  # Field2: Corn

# Load data from devices.json
def load_devices():
    try:
        with open("devices.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: devices.json file not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: devices.json contains invalid JSON.")
        return {}

# Update the UI with the latest data
def update_ui():
    devices = load_devices()

    # Clear existing device frames
    for widget in device_frame.winfo_children():
        widget.destroy()

    # Create frames for fields
    field1_frame = Frame(device_frame, bg="lightgreen", bd=2, relief="solid", padx=10, pady=10)
    field1_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    Label(field1_frame, text="Field 1: Wheat", font=("Arial", 16, "bold"), bg="lightgreen", fg="darkgreen").pack(anchor="w")

    field2_frame = Frame(device_frame, bg="lightyellow", bd=2, relief="solid", padx=10, pady=10)
    field2_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    Label(field2_frame, text="Field 2: Corn", font=("Arial", 16, "bold"), bg="lightyellow", fg="darkorange").pack(anchor="w")

    # Populate devices into fields
    for device_name, device_info in devices.items():
        # Extract device attributes
        index = device_info.get("index")
        state = device_info.get("state")
        config = device_info.get("config", {})
        value = config.get("value")
        battery = config.get("battery")
        pulse_counter = config.get("pulseCounter")

        # Skip devices without state and required config attributes
        if state is None and battery is None and pulse_counter is None and value is None:
            continue

        # Determine the field for the device
        if index in FIELD1_INDICES:
            parent_frame = field1_frame
        elif index in FIELD2_INDICES:
            parent_frame = field2_frame
        else:
            continue

        # Create a frame for each device
        device_container = Frame(parent_frame, bg="lightblue", bd=2, relief="solid", padx=10, pady=10)
        device_container.pack(fill="x", pady=5)

        # Add device name
        Label(device_container, text=f"{device_name}", font=("Arial", 14, "bold"), bg="lightblue", fg="darkblue").pack(anchor="w")

        # Display state if available
        if state is not None:
            Label(device_container, text=f"State: {state}", font=("Arial", 12), bg="lightblue", fg="green" if state == "ON" else "red").pack(anchor="w")
        if value is not None:
            Label(device_container, text=f"Value: {value}%", font=("Arial", 12), bg="lightblue", fg="black").pack(anchor="w")
        # Display battery and pulseCounter if available
        if battery is not None:
            Label(device_container, text=f"Battery: {battery}%", font=("Arial", 12), bg="lightblue", fg="black").pack(anchor="w")
        if pulse_counter is not None:
            Label(device_container, text=f"Pulse Counter: {pulse_counter}L", font=("Arial", 12), bg="lightblue", fg="black").pack(anchor="w")

    # Schedule the next update
    root.after(2000, update_ui)  # Update every 2 seconds

# Initialize the UI
root = Tk()
root.title("Irrigation System Monitor")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to 80% of the screen size
width = int(screen_width * 0.8)
height = int(screen_height * 0.7)

# Center the window
x = (screen_width - width) // 2
y = (screen_height - height) // 2

root.geometry(f"{width}x{height}+{x}+{y}")

# Create a frame to hold all devices
device_frame = Frame(root)
device_frame.pack(fill="both", expand=True)

# Configure grid layout for fields
device_frame.grid_columnconfigure(0, weight=1)  # Field 1
device_frame.grid_columnconfigure(1, weight=1)  # Field 2

# Start the UI update loop
update_ui()

# Run the Tkinter event loop
root.mainloop()