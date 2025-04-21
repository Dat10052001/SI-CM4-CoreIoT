# 🌱 Ứng Dụng Tưới Tiêu Thông Minh

## Giới Thiệu
Dự án này nhằm phát triển một hệ thống tưới tiêu thông minh sử dụng nền tảng CoreIOT kết hợp với mạch nhúng CM4 Raspberry PI. Hệ thống giúp tự động hóa quá trình tưới cây, tiết kiệm nước và tăng cường hiệu quả sản xuất nông nghiệp. 💧

## Tính Năng
- **Giám sát độ ẩm đất**: Sử dụng cảm biến để theo dõi độ ẩm của đất. 🌾
- **Điều khiển van tưới**: Tự động mở/đóng van tưới dựa trên dữ liệu từ cảm biến. 🔄
- **Giao diện người dùng**: Cung cấp giao diện thân thiện để người dùng có thể theo dõi và điều chỉnh hệ thống. 📱
- **Thông báo qua SMS/Email**: Gửi thông báo khi cần tưới hoặc có sự cố. 📧

## Công Nghệ Sử Dụng
- **Raspberry Pi CM4**: Mạch nhúng chính điều khiển hệ thống. 🖥️
- **CoreIOT**: Nền tảng IoT để quản lý thiết bị và dữ liệu. 🌐
- **Cảm biến độ ẩm**: Để đo độ ẩm của đất. 🌡️
- **Van điện từ**: Để điều khiển quá trình tưới tiêu. 🚰

## Cài Đặt
### Yêu Cầu Hệ Thống
- Raspberry Pi CM4
- Python 3.x
- Thư viện cần thiết: `gpiozero`, `requests`, `flask`

### Hướng Dẫn Cài Đặt
1. Cài đặt hệ điều hành cho Raspberry Pi. 🛠️
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install gpiozero requests flask
   ```
3. Clone repository về máy:
   ```bash
   git clone https://github.com/username/repo.git
   ```
4. Chạy ứng dụng:
   ```bash
   python app.py
   ```
## Sử Dụng
Truy cập vào địa chỉ IP của Raspberry Pi trên trình duyệt để mở giao diện người dùng. 🌍
Theo dõi độ ẩm và điều chỉnh cài đặt tưới tiêu theo nhu cầu. ⚙️

## Giấy Phép
Dự án này được cấp phép theo Giấy phép MIT. Vui lòng xem file LICENSE để biết thêm chi tiết. 📜

## Liên Hệ
Nếu có bất kỳ câu hỏi nào, bạn có thể liên hệ qua email: example@example.com 📬
