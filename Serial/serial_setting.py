import serial.tools.list_ports

class Serial():
  def get_serial_port():
    # ports = serial.tools.list_ports.comports()
    # N = len(ports)
    # commPort = "None"
    # for i in range(0, N):
    #     port = ports[i]
    #     strPort = str(port)
    #     print(strPort) # print(strPort)
    #     if "FT232R USB UART" in strPort:
    #         splitPort = strPort.split(" ")
    #         print("PortName:",strPort)
    #         commPort = splitPort[0]
    # return commPort
    return "/dev/ttyUSB0"
  
  def get_serial_bandrate():
    return 9600
  
  def get_serial_baudrate_distance():
    return 19200