from customtkinter import *
from app.togglebutton import ToggleButton
from constant import *

sensor_data = [26, 47, 65, 842] # [temp, humi, ph, ec]

class Control_System(CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.parent = master
        self.serialCom = self.parent.task.system.serialCom

        self.configure(fg_color="transparent")
        self.grid_columnconfigure((0, 1), weight=1)  # Chia layout thành 2 cột
        self.grid_rowconfigure(0, weight=1)

        # === FRAME BÊN TRÁI ===
        self.left_frame = CTkFrame(self, fg_color="transparent", width=self.winfo_screenwidth() // 2)
        self.left_frame.grid(row=0, column=0, padx=5, pady=50, sticky="nsew")
        self.left_frame.grid_rowconfigure((0, 1, 2), weight=1)  # 3 hàng dọc
        self.left_frame.grid_columnconfigure(0, weight=1)

        # === SOLUTIONS ===
        self.mix_frame = self.create_section(
            title="SOLUTIONS", col=0,
            rows=[("SOLUTION 1", self.btn_valve_1_onClick),
                  ("SOLUTION 2", self.btn_valve_2_onClick),
                  ("SOLUTION 3", self.btn_valve_3_onClick)]
        )
        self.mix_frame.grid(row=0, column=0, sticky="nsew",padx=(0,300), pady=(0, 60))

        # === IRRIGATION AREAS ===
        self.region_frame = self.create_section(
            title="IRRIGATION AREAS", col=0,
            rows=[("AREA 1", self.btn_pump_flow_1_onClick),
                  ("AREA 2", self.btn_pump_flow_2_onClick),
                  ("AREA 3", self.btn_pump_flow_3_onClick)]
        )
        self.region_frame.grid(row=1, column=0, sticky="nsew", padx=(0,300), pady=(0, 60))

        # === MÁY BƠM ===
        self.pump_frame = self.create_section(
            title="PUMP CONTROLLER", col=0,
            rows=[("PUMP IN", self.btn_pump_1_onClick),
                  ("PUMP OUT", self.btn_pump_2_onClick)]
        )
        self.pump_frame.grid(row=2, column=0, sticky="nsew", padx=(0,300), pady=(0, 60))

        # === FRAME BÊN PHẢI ===
        self.right_frame = CTkFrame(self, fg_color="transparent", width=self.winfo_screenwidth() // 2)
        self.right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.right_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)  # 4 hàng dọc
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Thêm các giá trị TEMPARATURE, độ ẩm, đất, ánh sáng
        self.add_sensor_value(self.right_frame, "TEMPERATURE", f"{sensor_data[0]}°C", 0, bg_color="blue")
        self.add_sensor_value(self.right_frame, "HUMIDITY", f"{sensor_data[1]}%", 1, bg_color="green")
        self.add_sensor_value(self.right_frame, "SOIL MOISTURE", f"{sensor_data[0]}%", 2, bg_color="red")
        self.add_sensor_value(self.right_frame, "LIGHT", f"{sensor_data[0]} Lux", 3, bg_color="coral")

        self.update()

    def create_section(self, title, col, rows):
        frame = CTkFrame(self.left_frame, fg_color="transparent")  # Đặt trong left_frame
        frame.grid_columnconfigure(0, weight=1)

        title_label = CTkLabel(frame, text=title, font=("Arial", 40, "bold"))
        title_label.grid(row=0, column=0, padx=(300,0), pady=10)

        for i, (label_text, callback) in enumerate(rows, start=1):
            self._create_horizontal_toggle(frame, label_text, i, callback)  # Gọi hàm mới

        return frame

    def _create_horizontal_toggle(self, parent, label_text, index, command):
        container = CTkFrame(parent, fg_color="transparent")
        container.grid(row=index, column=0, pady=0, sticky="nsew")  # Giảm khoảng cách giữa các thành phần
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)  # Cột của label không giãn
        container.grid_columnconfigure(1, weight=0)  # Cột của button có thể giãn

        # Label
        label = CTkLabel(container, text=label_text, font=("Arial", 45))
        label.grid(row=0, column=0)  # Giảm khoảng cách ngang giữa label và button

        # Button
        button = ToggleButton(container)
        button.setClickEvent(command)
        button.button_place(row=0, column=1)  # Nút nằm ngang bên phải label

        # Lưu button vào thuộc tính của lớp
        attr_name = self._get_attr_name_from_label(label_text)
        setattr(self, attr_name, button)

    def _get_attr_name_from_label(self, label):
        return "btn_" + "_".join(label.lower().replace(" ", "_").split())

    def add_sensor_value(self, parent, label_text, value_text, row, bg_color):
        container = CTkFrame(parent, fg_color=bg_color, corner_radius=10, width=self.winfo_screenwidth() // 4)
        container.grid(row=row, column=0, padx=10, pady=5, sticky="nsew")
        container.grid_rowconfigure((0, 1), weight=1)
        container.grid_columnconfigure((0,1,2), weight=1)

        label = CTkLabel(container, text=label_text, font=("Arial", 40, "bold"), fg_color=bg_color,text_color="white")
        label.grid(row=0, column=1, pady=(15, 0), sticky="nsew")

        value = CTkLabel(container, text=value_text, font=("Arial", 45), corner_radius=5,text_color="white")
        value.grid(row=1, column=1, pady=(0, 15), sticky="nsew")

    def update(self):
        self.system_state = self.parent.task.system.serialCom.relay_status

        # Cập nhật trạng thái các nút
        self.btn_solution_1.update_button_click(self.system_state[1])
        self.btn_solution_2.update_button_click(self.system_state[2])
        self.btn_solution_3.update_button_click(self.system_state[3])
        self.btn_area_1.update_button_click(self.system_state[4])
        self.btn_area_2.update_button_click(self.system_state[5])
        self.btn_area_3.update_button_click(self.system_state[6])
        self.btn_pump_in.update_button_click(self.system_state[7])

        # Kiểm tra trạng thái của các area
        area_open = any([self.system_state[4], self.system_state[5], self.system_state[6]])

        # Điều khiển pump_out dựa trên trạng thái của các area
        self.serialCom.control_relay(PUMP_2, area_open)
        self.btn_pump_out.update_button_click(area_open)

        # Lặp lại cập nhật sau 1000ms
        self.after(1000, self.update)

    def btn_valve_1_onClick(self, state): self.serialCom.control_relay(RELAY_1, state)
    def btn_valve_2_onClick(self, state): self.serialCom.control_relay(RELAY_2, state)
    def btn_valve_3_onClick(self, state): self.serialCom.control_relay(RELAY_3, state)
    def btn_pump_flow_1_onClick(self, state): self.serialCom.control_relay(RELAY_4, state)
    def btn_pump_flow_2_onClick(self, state): self.serialCom.control_relay(RELAY_5, state)
    def btn_pump_flow_3_onClick(self, state): self.serialCom.control_relay(RELAY_6, state)
    def btn_pump_1_onClick(self, state): self.serialCom.control_relay(PUMP_1, state)
    def btn_pump_2_onClick(self, state): self.serialCom.control_relay(PUMP_2, state)
