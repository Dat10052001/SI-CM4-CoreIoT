from ping3 import ping
import speedtest
import requests

def check_ping(host="google.com"):
    try:
        response = ping(host, timeout=2)  # Thêm timeout để tránh treo
        if response is None:
            print(f"Không thể kết nối đến {host}")
        else:
            print(f"Kết nối đến {host} thành công với thời gian {response:.2f} ms")
    except PermissionError as e:
        print(f"Lỗi quyền truy cập khi thực hiện ping đến {host}: {e}")
    except Exception as e:
        print(f"Lỗi khi thực hiện ping đến {host}: {e}")

def check_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        download_speed = st.download() / 1_000_000  # Mbps
        upload_speed = st.upload() / 1_000_000  # Mbps
        ping = st.results.ping  # ms

        print(f"Tốc độ tải xuống: {download_speed:.2f} Mbps")
        print(f"Tốc độ tải lên: {upload_speed:.2f} Mbps")
        print(f"Độ trễ (ping): {ping} ms")
    except speedtest.SpeedtestException as e:
        print(f"Lỗi khi kiểm tra tốc độ mạng: {e}")
    except Exception as e:
        print(f"Lỗi không mong muốn khi kiểm tra tốc độ mạng: {e}")

def check_http():
    try:
        response = requests.get("https://www.google.com", timeout=5)  # Thêm timeout
        if response.status_code == 200:
            print("Kết nối Internet ổn định.")
        else:
            print(f"Lỗi HTTP: {response.status_code}")
    except requests.exceptions.Timeout:
        print("Kết nối đến máy chủ bị timeout.")
    except requests.exceptions.RequestException as e:
        print(f"Không thể kết nối Internet: {e}")

def main():
    try:
        print("🔄 Kiểm tra kết nối mạng...")
        check_ping()
        print("\n🔄 Kiểm tra tốc độ mạng...")
        check_speed()
        print("\n🔄 Kiểm tra kết nối HTTP...")
        check_http()
    except PermissionError as e:
        print(f"Lỗi quyền truy cập: {e}")
    except Exception as e:
        print(f"Lỗi không mong muốn: {e}")

if __name__ == "__main__":
    main()
