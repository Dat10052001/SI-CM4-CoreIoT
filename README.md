# React Native Project

## Giới thiệu
Dự án này là một ứng dụng di động được xây dựng bằng React Native.

## Yêu cầu hệ thống
- Node.js (phiên bản mới nhất hoặc LTS)
- npm hoặc yarn
- React Native CLI hoặc Expo CLI (tuỳ vào cách triển khai)
- Android Studio (nếu chạy trên Android)
- Xcode (nếu chạy trên iOS)

## Cài đặt

Clone repo về máy:
```sh
git clone https://github.com/your-repo-name.git
cd your-repo-name
```

Cài đặt dependencies:
```sh
npm install
# hoặc
yarn install
```

## Chạy ứng dụng

Chạy trên Android:
```sh
npx react-native run-android
```

Chạy trên iOS:
```sh
npx react-native run-ios
```

Chạy bằng Expo:
```sh
npx expo start
```

## Cấu trúc thư mục
```
/your-project
├── android/         # Code native cho Android
├── ios/             # Code native cho iOS
├── src/             # Thư mục chứa source code chính
│   ├── components/  # Các component dùng chung
│   ├── screens/     # Các màn hình chính
│   ├── navigation/  # Điều hướng ứng dụng
│   ├── assets/      # Ảnh, icon, font,...
│   ├── utils/       # Các hàm tiện ích
├── App.js           # Entry point của ứng dụng
├── package.json     # File cấu hình dependencies
└── README.md        # Tài liệu hướng dẫn
```

## Công nghệ sử dụng
- React Native
- React Navigation
- Redux (nếu cần quản lý state)
- Axios (gọi API)
- AsyncStorage (lưu trữ dữ liệu cục bộ)

## Đóng góp
Nếu bạn muốn đóng góp vào dự án, hãy fork repo và tạo pull request!

## Giấy phép
Dự án này được cấp phép theo MIT License.

