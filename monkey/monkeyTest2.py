# 未跑通，deviceservice连接有问题待修改，多包monkey
# byShirley 2023.06.12,待调试
import os
import subprocess
import threading
import time

DEVICE_SERIAL = "127.0.0.1:7555"  # 设备序列号
MONKEY_SEED = 1234  # Monkey测试种子
MONKEY_EVENTS = 10000  # Monkey测试事件数
MONKEY_TIMEOUT = 10  # Monkey测试超时时间（秒）
LOG_DIR = "d:\\monkeylog"  # 日志保存目录

# 应用包名列表
PACKAGE_LIST = [
    "com.example.package1",
    "com.example.package2",
    "com.example.package3"
]

def run_command(command):
    """运行shell命令"""
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = p.communicate()
    return output.decode(), error.decode()

def connect_device():
    """连接设备"""
    output, error = run_command(f"adb connect \'{DEVICE_SERIAL}\'")

    if "connected to" in output:
        print(f"Device \'{DEVICE_SERIAL}\' connected successfully!")
    else:
        print(f"Failed to connect device \'{DEVICE_SERIAL}\'!")
        print(f"Error message: {error}")

def disconnect_device():
    """断开设备连接"""
    output, error = run_command(f"adb disconnect \'{DEVICE_SERIAL}\'")
    if "disconnected" in output:
        print(f"Device \'{DEVICE_SERIAL}\'  disconnected successfully!")
    else:
        print(f"Failed to disconnect device \'{DEVICE_SERIAL}\' !")
        print(f"Error message: {error}")

def start_monkey(package):
    """启动Monkey测试"""
    print(f"Starting Monkey test for package {package}...")
    timestamp = int(time.time())
    log_file = os.path.join(LOG_DIR, f"monkey_{package}_{timestamp}.txt")
    output, error = run_command(f"adb shell monkey -s {MONKEY_SEED} -p {package} -v {MONKEY_EVENTS} --throttle 500 --ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes --monitor-native-crashes --pct-touch 50 --pct-motion 25 --pct-nav 10 --pct-majornav 10 --pct-appswitch 5 --pct-anyevent 0 > {log_file}")
    if error:
        print(f"Monkey test for package {package} failed with error: {error}")
    else:
        print(f"Monkey test for package {package} completed successfully!")
    disconnect_device()

def capture_screenshot(package):
    """截图"""
    timestamp = int(time.time())
    screenshot_file = os.path.join(LOG_DIR, f"screenshot_{package}_{timestamp}.png")
    run_command(f"adb shell screencap -p /sdcard/screenshot.png")
    run_command(f"adb pull /sdcard/screenshot.png {screenshot_file}")
    print(f"Screenshot for package {package} saved to {screenshot_file}")

def capture_video(package):
    """录屏"""
    timestamp = int(time.time())
    video_file = os.path.join(LOG_DIR, f"video_{package}_{timestamp}.mp4")
    run_command(f"adb shell screenrecord /sdcard/video.mp4")
    run_command(f"adb pull /sdcard/video.mp4 {video_file}")
    print(f"Video for package {package} saved to {video_file}")

def parse_logs(package):
    """解析Monkey测试日志"""
    print(f"Parsing logs for package {package}...")
    timestamp = int(time.time())
    log_file = os.path.join(LOG_DIR, f"monkey_{package}_{timestamp}.txt")
    with open(log_file, "r") as f:
        lines = f.readlines()
    for line in lines:
        if "CRASH" in line:
            # 提取错误信息和时间戳
            error_message = line.split(":")[1].strip()
            time_stamp = line.split()[0]
            # 记录日志
            log = f"[{time_stamp}] CRASH: {error_message}"
            print(log)
            # 截图
            capture_screenshot()
            # 录屏
            capture_video()
            # 保存日志
            log_file = os.path.join(LOG_DIR, f"crash_{time_stamp}.txt")
            with open(log_file, "w") as f:
                f.write(log)
            print(f"Crash log saved to {log_file}")

