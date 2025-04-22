import threading
import requests
import json
import os
from datetime import datetime
from threading import Event

HOST = "https://app.coreiot.io"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOILMOISTURE_FILE = os.path.join(BASE_DIR, "SoilMoisture.json")
SMARTVALVE_FILE = os.path.join(BASE_DIR, "SmartValve.json")
WATERMETER_FILE = os.path.join(BASE_DIR, "WaterMeter.json")
DATA_FILE = os.path.join(BASE_DIR, "processed_data.json")

time_to_sent = 10

def log(name, message):
    timestamp = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
    log_message = f"[{timestamp}] [{name}] [{message}]"
    print(log_message, flush=True)  # Vẫn in ra màn hình
    try:
        # Ghi log vào file log.txt
        with open("log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(log_message + "\n")
    except Exception as e:
        print(f"❌ Failed to write log to file: {e}", flush=True)

def load_device_file(file_path):
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        log("system", f"❌ Failed to load file {file_path} {e}")
        return {}

def save_device_file(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        log("system", f"❌ Failed to save file {file_path} {e}")

def format_data(data):
    return "[" + ", ".join(f"{k} = {v}" for k, v in data.items()) + "]"

def send_telemetry(api_base, headers, name, data):
    try:
        url = f"{api_base}/telemetry"
        r = requests.post(url, headers=headers, json=data)
        if r.status_code == 200:
            log(name, f"🔺 Sent telemetry {format_data(data)}")
        else:
            log(name, f"⚠️ Telemetry error {r.status_code}: {r.text}")
    except Exception as e:
        log(name, f"❌ Telemetry exception {e}")

def send_attributes(api_base, headers, name, data):
    try:
        url = f"{api_base}/attributes"
        r = requests.post(url, headers=headers, json=data)
        if r.status_code == 200:
            log(name, f"🔺 Sent attributes {format_data(data)}")
        else:
            log(name, f"⚠️ Attribute error {r.status_code}: {r.text}")
    except Exception as e:
        log(name, f"❌ Attribute exception {e}")


def listen_rpc_valve(device):
    name = device["name"]
    access_token = device["access_token"]
    api_base = f"{HOST}/api/v1/{access_token}"
    headers = {"Content-Type": "application/json"}
    url = f"{api_base}/rpc?timeout=60000"
    wait_event = Event()  # Tạo một Event để chờ

    log(name, "📞 Listening RPC...")

    while True:
        try:
            r = requests.get(url, timeout=65)
            if r.status_code == 200:
                rpc = r.json()
                method = rpc.get("method")
                params = rpc.get("params")
                methodText = "Turned On" if method == "TURN_ON" else "Turned Off"
                paramsText = f"Params: {params}" if params else "No Params"
                log(name, f"⬇️  RPC received → {methodText} & {paramsText}")

                if method == "TURN_ON":
                    device["state"] = "ON"
                elif method == "TURN_OFF":
                    device["state"] = "OFF"

                # Tải file hiện tại
                state_data = load_device_file(SMARTVALVE_FILE)

                # Cập nhật đúng valve theo tên
                if name == "SI Smart Valve 1":
                    state_data["SI Smart Valve 1"] = device
                elif name == "SI Smart Valve 2":
                    state_data["SI Smart Valve 2"] = device

                # Ghi lại file
                save_device_file(SMARTVALVE_FILE, state_data)

                send_attributes(api_base, headers, name, {"state": device["state"]})
            elif r.status_code == 408:
                log(name, "⏳ RPC timeout")
        except Exception as e:
            log(name, f"❌ RPC error: {e}")
        wait_event.wait(0.5)
        

def run_water_meter(device):
    """Lắng nghe SI Water Meter và tải dữ liệu"""
    name = device["name"]
    access_token = device["access_token"]
    api_base = f"{HOST}/api/v1/{access_token}"
    headers = {"Content-Type": "application/json"}
    wait_event = Event()  # Tạo một Event để chờ

    log(name, "🚀 Connected with device")

    while True:
        telemetry = {}
        config = device.get("config", {})
        # increment = config.get("increment", 1)
        increment = 1

        # Đọc trạng thái valve từ file JSON
        water_meter_devices = load_device_file(WATERMETER_FILE)
        smart_valve_devices = load_device_file(SMARTVALVE_FILE)
        is_water_meter_1 = (name == "SI Water Meter 1")
        is_water_meter_2 = (name == "SI Water Meter 2")
        valve_state1 = smart_valve_devices.get("SI Smart Valve 1").get("state", "OFF")
        valve_state2 = smart_valve_devices.get("SI Smart Valve 2").get("state", "OFF")

        if is_water_meter_1 and valve_state1 == "ON":
            # Nếu valve_state == "ON", tải cả "battery" và "pulseCounter" mỗi 1s
            pulse_counter1 = water_meter_devices["SI Water Meter 1"]["config"]["pulseCounter"]
            pulse_counter1 += increment
            water_meter_devices["SI Water Meter 1"]["config"]["pulseCounter"] = pulse_counter1
            save_device_file(WATERMETER_FILE, water_meter_devices)
            telemetry = {
                "battery": config.get("battery", 0),
                "pulseCounter": pulse_counter1,
            }
            send_telemetry(api_base, headers, name, telemetry)

        if is_water_meter_2 and valve_state2 == "ON":
            # Nếu valve_state == "ON", tải cả "battery" và "pulseCounter" mỗi 1s
            pulse_counter2 = water_meter_devices["SI Water Meter 2"]["config"]["pulseCounter"]
            pulse_counter2 += increment
            water_meter_devices["SI Water Meter 2"]["config"]["pulseCounter"] = pulse_counter2
            save_device_file(WATERMETER_FILE, water_meter_devices)
            telemetry = {
                "battery": config.get("battery", 0),
                "pulseCounter": pulse_counter2,
            }
            send_telemetry(api_base, headers, name, telemetry)

        if valve_state1 == "OFF" and valve_state2 == "OFF":
            # Nếu valve_state != "ON", chỉ tải "battery" mỗi 5s
            telemetry = {"battery": config.get("battery", 0)}
            send_telemetry(api_base, headers, name, telemetry)
            wait_event.wait(time_to_sent - 1)
  # Chờ 5 giây mà không chặn chương trình
        wait_event.wait(0.5)

def run_other_device(device):
    """Lắng nghe các thiết bị khác và giữ logic như cũ"""
    name = device["name"]
    access_token = device["access_token"]
    api_base = f"{HOST}/api/v1/{access_token}"
    headers = {"Content-Type": "application/json"}
    wait_event = Event()
    log(name, "🚀 Connected with device")

    if name.startswith("SI Smart Valve"):
        threading.Thread(target=listen_rpc_valve, args=(device,), daemon=True).start()

    while True:
        telemetry = {}
        config = device.get("config", {})
        calibrate = config.get("calibrate")
        accuracy = config.get("accuracy")
        name = device["name"]

        soil_data = load_device_file(DATA_FILE)
        if device.get("enable_telemetry") and calibrate and accuracy:
            for sensor_name, factor in calibrate.items():
                    # raw = random.uniform(0.8, 1)
                    # telemetry[sensor_name] = round(raw * factor, accuracy.get(sensor_name, 1))
                for key, sensor in soil_data.items():
                    if name == key:
                        telemetry[sensor_name] = sensor["value"]
                                  
        # Thêm giá trị battery vào telemetry nếu có
        if "battery" in config:
            telemetry["battery"] = config["battery"]

        elif config:
            telemetry = config

        # Lọc các giá trị cần thiết
        telemetry = {k: v for k, v in telemetry.items() if k in ("battery", "moisture")}

        # Gửi telemetry
        send_telemetry(api_base, headers, name, telemetry)
        wait_event.wait(time_to_sent)

def main():
    # Load devices from the new JSON files
    soil_moisture = load_device_file(SOILMOISTURE_FILE)
    smart_valve = load_device_file(SMARTVALVE_FILE)
    water_meter = load_device_file(WATERMETER_FILE)

    # Combine all devices into a single list
    devices = list(smart_valve.values()) + list(water_meter.values()) + list(soil_moisture.values())

    if not devices:
        log("system", "❌ No devices found in the JSON files")
        return

    threads = []
    for device in devices:
        if device["name"].startswith("SI Water Meter"):
            # Chạy hàm xử lý SI Water Meter
            t = threading.Thread(target=run_water_meter, args=(device,))
        else:
            # Chạy hàm xử lý các thiết bị khác
            t = threading.Thread(target=run_other_device, args=(device,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()

