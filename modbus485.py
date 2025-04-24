import time
import serial
import threading

class SerialCommunicate:
    def __init__(self, RSport, RSbaudrate):
        self.RSport = RSport
        self.RSbaudrate = RSbaudrate

        self.relay_ON = [
            None,
            [1, 5, 0, 0, 255, 0, 140, 58],
            [1, 5, 0, 1, 255, 0, 221, 250],
        ]

        self.relay_OFF = [
            None,
            [1, 5, 0, 0, 0, 0, 205, 202],
            [1, 5, 0, 1, 0, 0, 156, 10],
        ]

        try:
            self.serRS = serial.Serial(port=self.RSport, baudrate=self.RSbaudrate, timeout=1)
            print(f"✅ Đã kết nối tới {self.RSport}")
        except serial.SerialException as e:
            print(f"❌ Không thể mở cổng {self.RSport}: {e}")
            exit(1)

    def send_relay_command(self, command):
        if self.serRS.isOpen():
            self.serRS.write(bytes(command))
        else:
            print("❌ Cổng RS485 không mở")

    def toggle_relay(self, relay_number, state):
        command = self.relay_ON[relay_number] if state else self.relay_OFF[relay_number]
        status = "ON" if state else "OFF"
        print(f"🔁 Relay {relay_number} {status}")
        self.send_relay_command(command)
        time.sleep(2)

    def run(self):
        """Chạy relay 1 mỗi 2 giây, relay 2 mỗi 3 giây song song"""
        try:
            t1 = threading.Thread(target=self.toggle_relay(1, True))
            t2 = threading.Thread(target=self.toggle_relay(2, True))
            t3 = threading.Thread(target=self.toggle_relay(1, False)) 
            t4 = threading.Thread(target=self.toggle_relay(2, False))
            t1.daemon = True  # Đảm bảo các luồng sẽ dừng khi chương trình dừng
            t2.daemon = True
            t3.daemon = True  # Đảm bảo các luồng sẽ dừng khi chương trình dừng
            t4.daemon = True
            t1.start()  # Khởi chạy luồng Relay 1
            t2.start()
            t3.start()  # Khởi chạy luồng Relay 1
            t4.start()
            t1.join()  # Chờ Relay 1
            t2.join()
            t3.join()  # Chờ Relay 1
            t4.join()
        except KeyboardInterrupt:
            print("🛑 Dừng chương trình.")
        finally:
            self.serRS.close()
            print("🔌 Đã ngắt kết nối.")

if __name__ == "__main__":
    RSport = "/dev/ttyUSB0"  # Hoặc cổng đúng của bạn (ví dụ: /dev/ttyUSB1)
    RSbaudrate = 9600

    comm = SerialCommunicate(RSport, RSbaudrate)
    comm.run()
