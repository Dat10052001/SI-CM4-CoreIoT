import subprocess

def main():
    # Chạy thingboard.py
    process1 = subprocess.Popen(["python3", "components/thingboard.py"])
    
    # Chạy thingboard_UI.py
    process2 = subprocess.Popen(["python3", "components/thingboard_UI.py"])
    
    # Đợi cả hai process kết thúc (nếu cần)
    process1.wait()
    process2.wait()

if __name__ == "__main__":
    main()