import serial
import threading

class SerialCommunicate:
    def __init__(self, RSport, RSbaudrate):
        self.RSport = RSport
        self.RSbaudrate = RSbaudrate
        self.lock = threading.Lock()  # Lock to ensure safe communication

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
            print(f"Connected to {self.RSport}")
        except serial.SerialException as e:
            print(f"Failed to open port {self.RSport}: {e}")
            exit(1)

    def send_relay_command(self, command):
        with self.lock:  # Ensure only one command is sent at a time
            if self.serRS.isOpen():
                self.serRS.write(bytes(command))
            else:
                print("RS485 port is not open")

    def toggle_relay(self, relay_number, state):
        if relay_number not in [1, 2]:
            print(f"Invalid relay {relay_number}")
            return

        command = self.relay_ON[relay_number] if state else self.relay_OFF[relay_number]
        status = "ON" if state else "OFF"
        print(f"Relay {relay_number} {status}")
        self.send_relay_command(command)

    def close(self):
        """Close RS485 connection"""
        if self.serRS.isOpen():
            self.serRS.close()
            print("RS485 connection closed.")

if __name__ == "__main__":
    RSport = "/dev/ttyUSB0"  # Or the correct port for your system
    RSbaudrate = 9600

    comm = SerialCommunicate(RSport, RSbaudrate)
    comm.toggle_relay(1, True)
    comm.toggle_relay(2, False)
    comm.close()
