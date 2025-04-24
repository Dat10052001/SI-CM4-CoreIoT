import time
import serial

class SerialCommunicate:
    def __init__(self, RSport, RSbaudrate):
        self.RSport = RSport
        self.RSbaudrate = RSbaudrate
        
        self.relay_ON = [
            None,
            [1, 5, 0, 0, 255, 0, 140, 58],
            [1, 5, 0, 1, 255, 0, 221, 250],
            # Thêm các relay khác nếu cần
        ]
        
        self.relay_OFF = [
            None,
            [1, 5, 0, 0, 0, 0, 205, 202],
            [1, 5, 0, 1, 0, 0, 156, 10],
            # Thêm các relay khác nếu cần
        ]
        
        # Khởi tạo cổng RS485 (serial)
        self.serRS = serial.Serial(port=self.RSport, baudrate=self.RSbaudrate, timeout=1)

    def send_relay_command(self, command):
        """Gửi lệnh bật/tắt relay qua RS485"""
        if self.serRS.isOpen():
            self.serRS.write(bytes(command))  # Gửi lệnh dưới dạng byte
            print(f"Đã gửi lệnh: {command}")
        else:
            print("❌ Cổng RS485 không mở")

    def toggle_relay(self, relay_number, state):
        """Bật/tắt relay dựa trên trạng thái"""
        if state:
            command = self.relay_ON[relay_number]
            print(f"✅ Relay {relay_number} ON")
        else:
            command = self.relay_OFF[relay_number]
            print(f"❌ Relay {relay_number} OFF")
        
        self.send_relay_command(command)

def run(self):
    """Chạy chương trình bật/tắt relay 1 mỗi 2 giây và relay 2 mỗi 3 giây"""
    try:
        while True:
            # Bật Relay 1
            self.toggle_relay(1, True)  # Bật Relay 1
            time.sleep(2)  # Đợi 2 giây
            self.toggle_relay(1, False)  # Tắt Relay 1
            time.sleep(2)  # Đợi 2 giây

            # Bật Relay 2
            self.toggle_relay(2, True)  # Bật Relay 2
            time.sleep(3)  # Đợi 3 giây
            self.toggle_relay(2, False)  # Tắt Relay 2
            time.sleep(3)  # Đợi 3 giây
    except KeyboardInterrupt:
        print("🛑 Dừng chương trình.")
    finally:
        self.serRS.close()
        print("🔌 Đã ngắt kết nối.")

# Tạo đối tượng SerialCommunicate và chạy
if __name__ == "__main__":
    RSport = "COM8"  # Cổng RS485 (cổng COM đang sử dụng)
    RSbaudrate = 9600  # Tốc độ baudrate (thường là 9600)

    comm = SerialCommunicate(RSport, RSbaudrate)
    comm.run()