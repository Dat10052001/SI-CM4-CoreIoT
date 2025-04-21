import json
from device_config import devices  # Import the devices list from device_config.py

# Filepath for devices.json
json_file_path = "devices.json"

# Load the existing data from devices.json
def load_json_data(filepath):
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: {filepath} not found. Creating a new file.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: {filepath} contains invalid JSON.")
        return {}

# Save updated data to devices.json
def save_json_data(filepath, data):
    try:
        with open(filepath, "w") as file:
            json.dump(data, file, indent=2)
        print(f"Updated {filepath} successfully.")
    except Exception as e:
        print(f"Error saving {filepath}: {e}")

# Update devices.json with new data from device_config.py
def update_devices_json():
    # Load existing data from devices.json
    existing_data = load_json_data(json_file_path)

    # Convert the devices list from device_config.py into a dictionary
    devices_dict = {device["name"]: device for device in devices}

    # Update or add new devices from device_config.py
    for device_name, device_info in devices_dict.items():
        existing_data[device_name] = device_info

    # Save the updated data back to devices.json
    save_json_data(json_file_path, existing_data)

# Run the update
if __name__ == "__main__":
    update_devices_json()