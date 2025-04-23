import json
import customtkinter as ctk
from datetime import datetime
from PIL import Image, ImageTk
from customtkinter import CTkImage
import os

timestamp = datetime.now().strftime(" %d/%m/%Y  %H:%M:%S")
# Define fields based on indices
FIELD1_INDICES = {0, 1, 2, 3}  # Field1: Wheat
FIELD2_INDICES = {4, 5, 6, 7}  # Field2: Corn

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SMARTVALVE_FILE = os.path.join(BASE_DIR, "../JSONdata/SmartValve.json")
WATERMETER_FILE = os.path.join(BASE_DIR, "../JSONdata/WaterMeter.json")
PROCESSED_DATA_FILE = os.path.join(BASE_DIR, "../JSONdata/processed_data.json")

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
height = int(screen_height * 0.85)
x = (screen_width - width) // 2
y = (screen_height - height) // 2
root.geometry(f"{width}x{height}+{x}+{y}")

# Tải ảnh clock.png bằng CTkImage
clock_image = CTkImage(
    light_image=Image.open("image/clock.png"),
    size=(40, 40)  # Resize ảnh về kích thước phù hợp
)

# Tải ảnh wheat.png và corn.png bằng CTkImage
wheat_image = CTkImage(
    light_image=Image.open("image/wheat.png"),
    size=(25, 30)  # Resize ảnh về kích thước phù hợp
)

corn_image = CTkImage(
    light_image=Image.open("image/corn.png"),
    size=(40, 40)  # Resize ảnh về kích thước phù hợp
)

# Tải các biểu tượng bằng CTkImage
humid_image = CTkImage(
    light_image=Image.open("image/humid.png"),
    size=(20, 20)  # Resize ảnh về kích thước phù hợp
)

on_image = CTkImage(
    light_image=Image.open("image/on.png"),
    size=(20, 20)
)

off_image = CTkImage(
    light_image=Image.open("image/off.png"),
    size=(20, 20)
)

pulse_image = CTkImage(
    light_image=Image.open("image/pulseCounter.png"),
    size=(20, 20)
)

watermeter_image = CTkImage(
    light_image=Image.open("image/watermeter.png"),
    size=(30, 25)
)

valve_image = CTkImage(
    light_image=Image.open("image/valve.png"),
    size=(30, 25)
)

# Tải các ảnh pin bằng CTkImage
battery_1_image = CTkImage(
    light_image=Image.open("image/battery_1.png"),
    size=(20, 25)  # Resize ảnh về kích thước phù hợp
)

battery_2_image = CTkImage(
    light_image=Image.open("image/battery_2.png"),
    size=(20, 25)
)

battery_3_image = CTkImage(
    light_image=Image.open("image/battery_3.png"),
    size=(20, 25)
)

battery_4_image = CTkImage(
    light_image=Image.open("image/battery_4.png"),
    size=(20, 25)
)

# Hàm chọn ảnh pin dựa trên giá trị battery
def get_battery_image(battery):
    if battery <= 25:
        return battery_1_image
    elif battery <= 50:
        return battery_2_image
    elif battery <= 75:
        return battery_3_image
    else:
        return battery_4_image

# Đặt timestamp_label ở đầu giao diện với ảnh clock
timestamp_label = ctk.CTkLabel(
    root,
    text=timestamp,
    font=("Segoe UI", 25),
    text_color="#333333",
    image=clock_image,  # Thêm ảnh vào label
    compound="left"  # Hiển thị ảnh bên trái văn bản
)
timestamp_label.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")  # Đặt ở hàng đầu tiên, chiếm 2 cột

# Đặt scrollable_frame bên dưới timestamp_label
scrollable_frame = ctk.CTkScrollableFrame(root, width=width, height=height)
scrollable_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=0, pady=0)

# Cấu hình lưới cho root để đảm bảo bố cục
root.grid_rowconfigure(1, weight=1)  # Cho phép scrollable_frame mở rộng theo chiều dọc
root.grid_columnconfigure(0, weight=1)  # Cho phép các cột mở rộng theo chiều ngang

scrollable_frame.grid_columnconfigure(0, weight=1)
scrollable_frame.grid_columnconfigure(1, weight=1)

# Agriculture green: #a8d5ba, Water blue: #b3e0f2
# Field 1 - Wheat
field1_frame = ctk.CTkFrame(scrollable_frame, fg_color="#228b22", corner_radius=20)
field1_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
ctk.CTkLabel(
    field1_frame,
    text="Field 1 - Wheat ",
    font=SECTION_TITLE_FONT,
    text_color="#00ff7f",
    image=wheat_image,  # Thêm ảnh wheat
    compound="right"  # Hiển thị ảnh bên trái văn bản
).pack(anchor="w", padx=20, pady=(15, 10))

# Field 2 - Corn
field2_frame = ctk.CTkFrame(scrollable_frame, fg_color="#b3e0f2", corner_radius=20)
field2_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
ctk.CTkLabel(
    field2_frame,
    text="Field 2 - Corn ",
    font=SECTION_TITLE_FONT,
    text_color="#005580",
    image=corn_image,  # Thêm ảnh corn
    compound="right"  # Hiển thị ảnh bên trái văn bản
).pack(anchor="w", padx=20, pady=(15, 10))

# Lưu trạng thái hiện tại của các thiết bị và container
current_device_states = {}
device_containers = {}  # Dùng để lưu các container của từng thiết bị

# Cập nhật các giá trị state, value, battery, pulseCounter
def update_ui():
    global current_device_states, device_containers, timestamp_label

    # Cập nhật timestamp
    timestamp = datetime.now().strftime(" %d/%m/%Y  %H:%M:%S")
    timestamp_label.configure(text=timestamp)

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
            if device_name.startswith("SI Water Meter"):
                device_container.pack(fill="x", pady=(8, 20), padx=20)
                icon_image = watermeter_image
            elif device_name.startswith("SI Smart Valve"):
                device_container.pack(fill="x", pady=(8, 20), padx=20)
                icon_image = valve_image
            else:
                device_container.pack(fill="x", pady=8, padx=20)
                icon_image = valve_image
            device_containers[device_name] = device_container

            # Thêm tên thiết bị với biểu tượng
            ctk.CTkLabel(
                device_container,
                text=f"{device_name} ",
                font=DEVICE_NAME_FONT,
                text_color="#003366",
                image=icon_image,
                compound="right"
            ).pack(anchor="w", pady=(8, 4), padx=12)
        else:
            # Lấy container đã tồn tại
            device_container = device_containers[device_name]

        # Xóa các widget con cũ trong container (trừ tên thiết bị)
        for widget in device_container.winfo_children()[1:]:
            widget.destroy()

        # Cập nhật các giá trị state, value, battery, pulseCounter
        if state is not None:
            state_label = "ON" if state == "ON" else "OFF"
            state_image = on_image if state == "ON" else off_image
            ctk.CTkLabel(
                device_container,
                text=f" Status: {state_label}",
                font=DEVICE_VALUE_FONT,
                text_color="green" if state == "ON" else "red",
                image=state_image,
                compound="left"
            ).pack(anchor="w", padx=12)

        if value is not None:
            ctk.CTkLabel(
                device_container,
                text=f" Moisture: {value}%",
                font=DEVICE_VALUE_FONT,
                image=humid_image,
                compound="left"
            ).pack(anchor="w", padx=12)

        if pulse_counter is not None:
            ctk.CTkLabel(
                device_container,
                text=f" Total Today: {pulse_counter} ml",
                font=DEVICE_VALUE_FONT,
                image=pulse_image,
                compound="left"
            ).pack(anchor="w", padx=12)

        if battery is not None:
            ctk.CTkLabel(
                device_container,
                text=f" Battery: {battery}%",
                font=DEVICE_VALUE_FONT,
                image=get_battery_image(battery),
                compound="left"
            ).pack(anchor="w", padx=12, pady=(0, 8))

    # Lập lịch cập nhật tiếp theo
    root.after(1000, update_ui)

update_ui()
root.mainloop()
