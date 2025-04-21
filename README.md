🌱 Ứng Dụng Tưới Tiêu Thông Minh Dựa Trên Nền Tảng CoreIOT và Mạch Nhúng CM4 Raspberry Pi
📝 Mô Tả Dự Án
Dự án "Ứng dụng tưới tiêu thông minh" sử dụng nền tảng CoreIOT và mạch nhúng CM4 Raspberry Pi, nhằm cung cấp một giải pháp tự động hóa quá trình tưới tiêu trong nông nghiệp. Hệ thống tích hợp cảm biến môi trường, các công nghệ IoT hiện đại, giúp tối ưu hóa quá trình canh tác, tiết kiệm tài nguyên và tăng hiệu quả sản xuất 🌾.

Hệ thống cho phép giám sát từ xa thông qua giao diện trực quan và hỗ trợ điều khiển linh hoạt, phù hợp với các mô hình nông trại quy mô nhỏ đến lớn.

✨ Tính Năng Chính
Tự Động Tưới Tiêu 💧

Hoạt động dựa trên dữ liệu cảm biến như độ ẩm đất, nhiệt độ, và thời tiết.
Tưới hoặc ngừng tưới khi đạt ngưỡng được cấu hình.
Giám Sát Từ Xa 📡

Theo dõi dữ liệu cảm biến và trạng thái hệ thống qua giao diện web hoặc ứng dụng di động.
Hỗ trợ cảnh báo thời gian thực khi xảy ra sự cố.
Điều Khiển Thủ Công 🖲️

Cho phép bật/tắt hệ thống tưới từ xa khi cần thiết.
Tối Ưu Hóa Tài Nguyên ♻️

Tiết kiệm nước và năng lượng bằng cách tưới đúng lượng cần thiết.
Tích Hợp IoT 🌐

Lưu trữ dữ liệu trên nền tảng CoreIOT, hỗ trợ phân tích và dự báo xu hướng.
🔧 Công Nghệ Sử Dụng
Phần Cứng
Raspberry Pi Compute Module 4 (CM4): Trung tâm xử lý và điều khiển.
Cảm Biến:
Độ ẩm đất: Giám sát độ ẩm tại các khu vực trồng trọt.
Nhiệt độ, độ ẩm không khí: Theo dõi điều kiện môi trường.
Relay Module: Điều khiển bơm nước và các thiết bị ngoại vi.
Máy Bơm Nước: Hoạt động theo tín hiệu từ hệ thống.
Phần Mềm
CoreIOT: Nền tảng IoT giám sát và lưu trữ dữ liệu.
Python: Xử lý logic hệ thống và giao tiếp với phần cứng.
Flask/Django: Xây dựng API và giao diện web.
MQTT: Giao thức truyền thông IoT giữa các thiết bị.
📂 Cấu Trúc Dự Án
css

Copier
├── src/                   # Mã nguồn chính
│   ├── sensors/           # Giao tiếp với cảm biến
│   ├── controllers/       # Điều khiển bơm và relay
│   ├── web/               # API và giao diện web
│   ├── iot/               # Kết nối với CoreIOT
│   └── utils/             # Tiện ích hỗ trợ
├── docs/                  # Tài liệu dự án
├── configs/               # File cấu hình
├── tests/                 # Kiểm thử
└── README.md              # Tài liệu này
🚀 Hướng Dẫn Cài Đặt
Yêu Cầu Hệ Thống
Raspberry Pi CM4.
Python 3.9 trở lên.
Kết nối internet ổn định.
Các cảm biến và thiết bị ngoại vi được kết nối đúng cách.
Các Bước Cài Đặt
Clone dự án:

bash

Copier
git clone https://github.com/yourusername/smart-irrigation.git
cd smart-irrigation
Cài đặt thư viện:

bash

Copier
pip install -r requirements.txt
Cấu hình hệ thống:

Chỉnh sửa file cấu hình trong thư mục configs/ theo nhu cầu.
Khởi chạy hệ thống:

bash

Copier
python src/main.py
Truy cập giao diện web:

Mở trình duyệt và truy cập: http://<IP_RASPBERRY_PI>:5000.
📖 Hướng Dẫn Sử Dụng
Giao Diện Người Dùng 🌐

Truy cập giao diện web để theo dõi dữ liệu cảm biến và kiểm soát hệ thống.
Cài Đặt Ngưỡng Tưới ⚙️

Đặt các ngưỡng độ ẩm đất, thời gian tưới trong giao diện.
Giám Sát Dữ Liệu 📊

Xem biểu đồ dữ liệu, nhận cảnh báo qua email hoặc ứng dụng di động.
Điều Khiển Hệ Thống 🖲️

Bật/tắt máy bơm hoặc điều chỉnh chế độ hoạt động.
🤝 Đóng Góp
Chúng tôi khuyến khích mọi ý kiến đóng góp để cải thiện hệ thống này.
Vui lòng tạo Pull Request hoặc liên hệ qua email với nhóm phát triển.

👥 Tác Giả
Nguyễn Văn A - Phát triển phần mềm.
Trần Thị B - Tích hợp phần cứng.
Lê Văn C - Thiết kế hệ thống.
📜 Giấy Phép
Dự án này được phát hành dưới giấy phép MIT.

