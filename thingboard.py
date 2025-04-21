import requests
import json
import time
import random
import os
from datetime import datetime
from multiprocessing import Process
from threading import Thread

HOST = "https://app.coreiot.io"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(BASE_DIR, "devices.json")
time_to_sent_1l = 10

def log(name, message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{name}] {message}", flush=True)

def save_device_state(state_data):
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        log("system", f"❌ Failed to save state: {e}")

def load_device_state():
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    except Exception as e:
        log("system", f"❌ Failed to load state: {e}")
        return {}

def send_telemetry(api_base, headers, name, data):
    try:
        url = f"{api_base}/telemetry"
        r = requests.post(url, headers=headers, json=data)
        if r.status_code == 200:
            log(name, f"📤 Sent telemetry: {data}")
        else:
            log(name, f"⚠️ Telemetry error {r.status_code}: {r.text}")
    except Exception as e:
        log(name, f"❌ Telemetry exception: {e}")

def send_attributes(api_base, headers, name, data):
    try:
        url = f"{api_base}/attributes"
        r = requests.post(url, headers=headers, json=data)
        if r.status_code == 200:
            log(name, f"📤 Sent attributes: {data}")
        else:
            log(name, f"⚠️ Attribute error {r.status_code}: {r.text}")
    except Exception as e:
        log(name, f"❌ Attribute exception: {e}")

def listen_rpc_valve(device):
    name = device["name"]
    access_token = device["access_token"]
    api_base = f"{HOST}/api/v1/{access_token}"
    headers = {"Content-Type": "application/json"}
    url = f"{api_base}/rpc?timeout=60000"

    state_data = load_device_state()
    state_data[name] = device

    while True:
        try:
            r = requests.get(url, timeout=65)
            if r.status_code == 200:
                rpc = r.json()
                method = rpc.get("method")
                params = rpc.get("params")
                log(name, f"📩 RPC received → method: {method}, params: {params}")
                if method == "TURN_ON":
                    state_data[name]["state"] = "ON"
                elif method == "TURN_OFF":
                    state_data[name]["state"] = "OFF"
                send_attributes(api_base, headers, name, {"state": state_data[name]["state"]})
                save_device_state(state_data)
            elif r.status_code == 408:
                log(name, "⏳ RPC timeout")
        except Exception as e:
            log(name, f"❌ RPC error: {e}")
        time.sleep(1)

def run_device(device):
    name = device["name"]
    access_token = device["access_token"]
    api_base = f"{HOST}/api/v1/{access_token}"
    headers = {"Content-Type": "application/json"}

    log(name, "🚀 Started device")

    if name == "SI Smart Valve 1" or name == "SI Smart Valve 2":
        Thread(target=listen_rpc_valve, args=(device,), daemon=True).start()

    last_minute = -1
    while True:
        telemetry = {}
        config = device.get("config", {})

        # meter1: đọc trạng thái valve1 từ file JSON
        if name == "SI Water Meter 1":
            state_data = load_device_state()
            valve_state = state_data.get("SI Smart Valve 1", {}).get("state", "OFF")
            increment = device.get("increment", 1)
            if valve_state == "ON":
                config["pulseCounter"] += increment
            # Luôn lưu lại pulseCounter mới vào state_data (dù ON hay OFF)
            state_data["SI Water Meter 1"]["config"]["pulseCounter"] = config["pulseCounter"]
            save_device_state(state_data)
            telemetry = config

        elif name == "SI Water Meter 2":
            state_data = load_device_state()
            valve_state = state_data.get("SI Smart Valve 2", {}).get("state", "OFF")
            increment = device.get("increment", 1)
            if valve_state == "ON":
                config["pulseCounter"] += increment
            state_data["SI Water Meter 2"]["config"]["pulseCounter"] = config["pulseCounter"]
            save_device_state(state_data)
            telemetry = config

        else:
            calibrate = config.get("calibrate")
            accuracy = config.get("accuracy")
            if device.get("enable_telemetry") and calibrate and accuracy:
                for sensor, factor in calibrate.items():
                    raw = random.uniform(0.8, 1)
                    telemetry[sensor] = round(raw * factor, accuracy.get(sensor, 1))
            if "battery" in config:
                telemetry["battery"] = config["battery"]
            elif config:
                telemetry = config
                
        telemetry = {k: v for k, v in telemetry.items() if k in ("battery", "moisture", "pulseCounter")}
        send_telemetry(api_base, headers, name, telemetry)
        time.sleep(time_to_sent_1l)

if __name__ == "__main__":
    state_data = load_device_state()
    
    # Nếu chưa có thiết bị trong file thì cảnh báo
    if not state_data:
        log("system", "❌ No devices found in devices.json")
        exit(1)

    # Lấy danh sách thiết bị từ state_data (dict of {name: device})
    devices = list(state_data.values())

    processes = []
    for device in devices:
        p = Process(target=run_device, args=(device,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

