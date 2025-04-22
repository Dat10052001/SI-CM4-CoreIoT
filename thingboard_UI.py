import json
import customtkinter as ctk

# Define fields based on indices
FIELD1_INDICES = {0, 1, 2, 3}  # Field1: Wheat
FIELD2_INDICES = {4, 5, 6, 7}  # Field2: Corn

# File paths
PROCESSED_DATA_FILE = "processed_data.json"
SMARTVALVE_FILE = "SmartValve.json"
WATERMETER_FILE = "WaterMeter.json"

# Font settings
TITLE_FONT = ("Segoe UI", 35, "bold")
SECTION_TITLE_FONT = ("Segoe UI", 30, "bold")
DEVICE_NAME_FONT = ("Segoe UI", 20, "bold")
DEVICE_VALUE_FONT = ("Segoe UI", 20)

# Load data from multiple JSON files
def load_devices():
    devices = {}
    try:
        with open(PROCESSED_DATA_FILE, "r", encoding="utf-8") as file:
            processed_data = json.load(file)
            for device_name, device_info in processed_data.items():
                devices[device_name] = {
                    "index": device_info.get("index"),
                    "value": device_info.get("value"),
                    "battery": device_info.get("battery"),
                }
    except (FileNotFoundError, json.JSONDecodeError):
        pass

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
    except (FileNotFoundError, json.JSONDecodeError):
        pass

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
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return devices

# Initialize the UI
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("IRRIGATION MONITORING SYSTEM")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = int(screen_width * 0.6)
height = int(screen_height * 0.75)
x = (screen_width - width) // 2
y = (screen_height - height) // 2
root.geometry(f"{width}x{height}+{x}+{y}")

scrollable_frame = ctk.CTkScrollableFrame(root, width=width, height=height)
scrollable_frame.pack(fill="both", expand=True, padx=0, pady=0)
scrollable_frame.grid_columnconfigure(0, weight=1)
scrollable_frame.grid_columnconfigure(1, weight=1)

# Agriculture green: #a8d5ba, Water blue: #b3e0f2
field1_frame = ctk.CTkFrame(scrollable_frame, fg_color="#228b22", corner_radius=20)
field1_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
ctk.CTkLabel(field1_frame, text="Field 1 - Wheat", font=SECTION_TITLE_FONT, text_color="#00ff7f").pack(anchor="w", padx=20, pady=(15, 10))

field2_frame = ctk.CTkFrame(scrollable_frame, fg_color="#b3e0f2", corner_radius=20)
field2_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
ctk.CTkLabel(field2_frame, text="Field 2 - Corn", font=SECTION_TITLE_FONT, text_color="#005580").pack(anchor="w", padx=20, pady=(15, 10))

# Lưu trạng thái hiện tại của các thiết bị và container
current_device_states = {}
device_containers = {}  # Dùng để lưu các container của từng thiết bị

def update_ui():
    global current_device_states, device_containers
    devices = load_devices()

    for device_name, device_info in devices.items():
        index = device_info.get("index")
        state = device_info.get("state")
        value = device_info.get("value")
        battery = device_info.get("battery")
        pulse_counter = device_info.get("pulseCounter")

        # Kiểm tra nếu thiết bị đã tồn tại và không có thay đổi
        if device_name in current_device_states:
            previous_state = current_device_states[device_name]
            if (
                previous_state.get("state") == state and
                previous_state.get("value") == value and
                previous_state.get("battery") == battery and
                previous_state.get("pulseCounter") == pulse_counter
            ):
                continue  # Không cập nhật nếu không có thay đổi

        # Cập nhật trạng thái mới
        current_device_states[device_name] = {
            "state": state,
            "value": value,
            "battery": battery,
            "pulseCounter": pulse_counter,
        }

        # Xác định khung cha (Field 1 hoặc Field 2)
        parent_frame = field1_frame if index in FIELD1_INDICES else field2_frame

        # Tìm hoặc tạo container cho thiết bị
        if device_name not in device_containers:
            # Nếu chưa có container, tạo mới
            device_container = ctk.CTkFrame(parent_frame, fg_color="#f0f8ff", corner_radius=15)
            device_container.pack(fill="x", pady=8, padx=20)
            device_containers[device_name] = device_container

            # Thêm tên thiết bị
            ctk.CTkLabel(device_container, text=f"{device_name}", font=DEVICE_NAME_FONT, text_color="#003366").pack(anchor="w", pady=(8, 4), padx=12)
        else:
            # Lấy container đã tồn tại
            device_container = device_containers[device_name]

        # Xóa các widget con cũ trong container (trừ tên thiết bị)
        for widget in device_container.winfo_children()[1:]:
            widget.destroy()

        # Cập nhật các giá trị state, value, battery, pulseCounter
        if state is not None:
            state_label = "Status: ON" if state == "ON" else "Status: OFF"
            color = "green" if state == "ON" else "red"
            ctk.CTkLabel(device_container, text=state_label, font=DEVICE_VALUE_FONT, text_color=color).pack(anchor="w", padx=12)

        if value is not None:
            ctk.CTkLabel(device_container, text=f"Moisture: {value}%", font=DEVICE_VALUE_FONT).pack(anchor="w", padx=12)

        if battery is not None:
            ctk.CTkLabel(device_container, text=f"Battery: {battery}%", font=DEVICE_VALUE_FONT).pack(anchor="w", padx=12)

        if pulse_counter is not None:
            ctk.CTkLabel(device_container, text=f"Total Today: {pulse_counter} ml", font=DEVICE_VALUE_FONT).pack(anchor="w", padx=12)

    # Lập lịch cập nhật tiếp theo
    root.after(1000, update_ui)

update_ui()
root.mainloop()
