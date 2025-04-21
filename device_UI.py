import json
from tkinter import Tk, Label, Frame, Canvas, Scrollbar

# Define fields based on indices
FIELD1_INDICES = {0, 1, 2, 3}  # Field1: Wheat
FIELD2_INDICES = {4, 5, 6, 7}  # Field2: Corn

# File paths
PROCESSED_DATA_FILE = "processed_data.json"
SMARTVALVE_FILE = "SmartValve.json"
WATERMETER_FILE = "WaterMeter.json"

# Load data from multiple JSON files
def load_devices():
    devices = {}

    # Load processed_data.json
    try:
        with open(PROCESSED_DATA_FILE, "r", encoding="utf-8") as file:
            processed_data = json.load(file)
            for device_name, device_info in processed_data.items():
                devices[device_name] = {
                    "index": device_info.get("index"),
                    "value": device_info.get("value"),
                    "battery": device_info.get("battery"),
                }
    except FileNotFoundError:
        print(f"Error: {PROCESSED_DATA_FILE} file not found.")
    except json.JSONDecodeError:
        print(f"Error: {PROCESSED_DATA_FILE} contains invalid JSON.")

    # Load SmartValve.json
    try:
        with open(SMARTVALVE_FILE, "r", encoding="utf-8") as file:
            smart_valve_data = json.load(file)
            for device_name, device_info in smart_valve_data.items():
                if device_name not in devices:
                    devices[device_name] = {}
                devices[device_name].update({
                    "index": device_info.get("index"),
                    "state": device_info.get("state"),
                    "battery": device_info.get("config", {}).get("battery"),
                })
    except FileNotFoundError:
        print(f"Error: {SMARTVALVE_FILE} file not found.")
    except json.JSONDecodeError:
        print(f"Error: {SMARTVALVE_FILE} contains invalid JSON.")

    # Load WaterMeter.json
    try:
        with open(WATERMETER_FILE, "r", encoding="utf-8") as file:
            water_meter_data = json.load(file)
            for device_name, device_info in water_meter_data.items():
                if device_name not in devices:
                    devices[device_name] = {}
                devices[device_name].update({
                    "index": device_info.get("index"),
                    "pulseCounter": device_info.get("config", {}).get("pulseCounter"),
                    "battery": device_info.get("config", {}).get("battery"),
                })
    except FileNotFoundError:
        print(f"Error: {WATERMETER_FILE} file not found.")
    except json.JSONDecodeError:
        print(f"Error: {WATERMETER_FILE} contains invalid JSON.")

    return devices

# Initialize the UI
root = Tk()
root.title("Irrigation System Monitor")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to 80% of the screen size
width = int(screen_width * 0.55)
height = int(screen_height * 0.7)

# Center the window
x = (screen_width - width) // 2
y = (screen_height - height) // 2

root.geometry(f"{width}x{height}+{x}+{y}")

# Create a canvas for scrolling
canvas = Canvas(root)
canvas.pack(side="left", fill="both", expand=True)

# Add a vertical scrollbar
scrollbar = Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure the canvas to work with the scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a frame inside the canvas to hold all devices
device_frame = Frame(canvas)
canvas.create_window((0, 0), window=device_frame, anchor="nw")

# Configure grid layout for fields
device_frame.grid_columnconfigure(0, weight=1, minsize=500)  # Field 1 (tăng trọng số để chiếm nhiều không gian hơn)
device_frame.grid_columnconfigure(1, weight=1, minsize=500)  # Field 2 (tăng trọng số để chiếm nhiều không gian hơn)

# Update the UI with the latest data
def update_ui():
    devices = load_devices()

    # Clear existing device frames
    for widget in device_frame.winfo_children():
        widget.destroy()

    # Create frames for fields
    field1_frame = Frame(device_frame, bg="lightgreen", bd=2, relief="solid", padx=10, pady=10)
    field1_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  # sticky="nsew" để mở rộng theo cả chiều ngang và dọc
    Label(field1_frame, text="Field 1: Wheat", font=("Arial", 16, "bold"), bg="lightgreen", fg="darkgreen").pack(anchor="w")

    field2_frame = Frame(device_frame, bg="lightyellow", bd=2, relief="solid", padx=10, pady=10)
    field2_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")  # sticky="nsew" để mở rộng theo cả chiều ngang và dọc
    Label(field2_frame, text="Field 2: Corn", font=("Arial", 16, "bold"), bg="lightyellow", fg="darkorange").pack(anchor="w")

    # Populate devices into fields
    for device_name, device_info in devices.items():
        # Extract device attributes
        index = device_info.get("index")
        state = device_info.get("state")
        value = device_info.get("value")
        battery = device_info.get("battery")
        pulse_counter = device_info.get("pulseCounter")

        # Determine the field for the device
        if index in FIELD1_INDICES:
            parent_frame = field1_frame
        else:
            parent_frame = field2_frame

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
    root.after(1000, update_ui)  # Update every 3 seconds

# Start the UI update loop
update_ui()

# Run the Tkinter event loop
root.mainloop()