import json
import random
import time
import os

PROCESSED_DATA_FILE = "processed_data.json"

def update_random_values(file_path, min_value=40, max_value=50, min_battery=30, max_battery=100):
    """
    Cập nhật giá trị 'value' và 'battery' ngẫu nhiên trong khoảng [min_value, max_value] và [min_battery, max_battery] cho tất cả các thiết bị.

    Args:
        file_path (str): Đường dẫn tới file JSON.
        min_value (float): Giá trị nhỏ nhất cho 'value' (mặc định là 40).
        max_value (float): Giá trị lớn nhất cho 'value' (mặc định là 50).
        min_battery (int): Giá trị nhỏ nhất cho 'battery' (mặc định là 30).
        max_battery (int): Giá trị lớn nhất cho 'battery' (mặc định là 100).
    """
    try:
        # Kiểm tra file tồn tại
        if not os.path.exists(file_path):
            print(f"❌ File {file_path} không tồn tại.")
            return

        # Đọc nội dung file JSON
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Cập nhật giá trị 'value' và 'battery' ngẫu nhiên cho từng thiết bị
        for device_name, device_data in data.items():
            random_value = round(random.uniform(min_value, max_value), 2)
            random_battery = random.randint(min_battery, max_battery)
            device_data["value"] = random_value
            device_data["battery"] = random_battery
            print(f"✅ Đã cập nhật {device_name} với value = {random_value}, battery = {random_battery}")

        # Ghi lại file JSON
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Đã lưu các giá trị mới vào file {file_path}")

    except json.JSONDecodeError as e:
        print(f"❌ Lỗi đọc file JSON: {e}")
    except Exception as e:
        print(f"❌ Lỗi không mong muốn: {e}")

if __name__ == "__main__":
    print("🔄 Bắt đầu cập nhật giá trị ngẫu nhiên cho processed_data.json...")
    update_random_values(PROCESSED_DATA_FILE)