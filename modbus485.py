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
        try:
            self.serRS = serial.Serial(port=self.RSport, baudrate=self.RSbaudrate, timeout=1)
            print(f"✅ Đã kết nối tới {self.RSport}")
        except serial.SerialException as e:
            print(f"❌ Không thể mở cổng {self.RSport}: {e}")
            exit(1)

    def send_relay_command(self, command):
        """Gửi lệnh bật/tắt relay qua RS485"""
        if self.serRS.isOpen():
            self.serRS.write(bytes(command))
            print(f"📤 Đã gửi lệnh: {command}")
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
        """Chạy chương trình bật/tắt relay 1 mỗi 2s và relay 2 mỗi 3s"""
        try:
            while True:
                self.toggle_relay(1, True)
                time.sleep(2)
                self.toggle_relay(1, False)
                time.sleep(2)

                self.toggle_relay(2, True)
                time.sleep(3)
                self.toggle_relay(2, False)
                time.sleep(3)
        except KeyboardInterrupt:
            print("🛑 Dừng chương trình.")
        finally:
            self.serRS.close()
            print("🔌 Đã ngắt kết nối.")

# Khởi chạy nếu chạy trực tiếp
if __name__ == "__main__":
    RSport = "/dev/ttyUSB0"  # Cổng RS485 trên Raspberry Pi (có thể là ttyUSB1, ttyUSB2...)
    RSbaudrate = 9600

    comm = SerialCommunicate(RSport, RSbaudrate)
    comm.run()
