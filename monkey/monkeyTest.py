# byShirley 2023.06.12,python monkeydemo.py,单包monkey
# 修改app包名即可，包含连设备，抓log，截图，视频。
import os
import subprocess
import time
import threading

# 连接 adb 设备
def connect_device(device):
    if device!='':
        subprocess.call(['adb', 'disconnect'])
        subprocess.call(['adb', 'connect', device])
    else:
        subprocess.call(['adb', 'shell'])

# 执行 monkey 测试
def run_monkey(package_name, event_count):
    subprocess.call(['adb', 'shell', 'monkey', '-p', package_name, str(event_count),'--throttle 500 --ignore-crashes --ignore-timeouts --ignore-security-exceptions --ignore-native-crashes --monitor-native-crashes'])

# 获取 logcat 日志
def get_logcat(tag=None):
    cmd = ['adb', 'logcat', '-d']
    if tag:
        cmd += ['-s', tag]
    output = subprocess.check_output(cmd)
    return output.decode()

# 获取错误信息和时间点
def get_errors_and_timestamps(logcat_output):
    errors = []
    timestamps = []
    for line in logcat_output.splitlines():
        if 'FATAL EXCEPTION' in line:
            errors.append(line)
            timestamp = line.split()[0]
            timestamps.append(timestamp)
    return errors, timestamps

# 截图线程
class ScreenshotThread(threading.Thread):
    def __init__(self, package_name, timestamp, output_dir):
        super().__init__()
        self.package_name = package_name
        self.timestamp = timestamp
        self.output_dir = output_dir

    def run(self):
        output_file = '{}_{}.png'.format(self.package_name, self.timestamp)
        subprocess.call(['adb', 'shell', 'screencap', '-p', '/sdcard/{}'.format(output_file)])
        subprocess.call(['adb', 'pull', '/sdcard/{}'.format(output_file), os.path.join(self.output_dir, output_file)])
        subprocess.call(['adb', 'shell', 'rm', '/sdcard/{}'.format(output_file)])

# 录制视频线程
class RecordThread(threading.Thread):
    def __init__(self, package_name, timestamp, output_dir):
        super().__init__()
        self.package_name = package_name
        self.timestamp = timestamp
        self.output_dir = output_dir

    def run(self):
        output_file = '{}_{}.mp4'.format(self.package_name, self.timestamp)
        subprocess.call(['adb', 'shell', 'screenrecord', '--time-limit', '10', '/sdcard/{}'.format(output_file)])
        subprocess.call(['adb', 'pull', '/sdcard/{}'.format(output_file), os.path.join(self.output_dir, output_file)])
        subprocess.call(['adb', 'shell', 'rm', '/sdcard/{}'.format(output_file)])



# 保存 logcat 日志和错误信息到文件
def save_logcat_and_errors(logcat_output, errors, output_dir):
    with open(os.path.join(output_dir, 'logcat.txt'), 'w') as f:
        f.write(logcat_output)
    with open(os.path.join(output_dir, 'errors.txt'), 'w') as f:
        for error in errors:
            f.write(error + '\n')

# 示例用法
if __name__ == '__main__':
    device = '127.0.0.1:7555'# 或直接使用 'adb shell' 命令连接设备
    package_name = 'com.tencent.mobileqq'
    event_count = 10000
    output_dir = 'D:/monkeylog'

    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 连接 adb 设备
    connect_device(device)
    # 执行 monkey 测试
    monkey_thread = threading.Thread(target=run_monkey, args=(package_name, event_count))
    monkey_thread.start()

    # 等待 monkey 测试结束
    monkey_thread.join()
    
    # 获取 logcat 日志
    logcat_output = get_logcat()

    # 获取错误信息和时间点
    errors, timestamps = get_errors_and_timestamps(logcat_output)
    if errors:
        print('Errors:')
        for error in errors:
            print(error)
        # 启动截图和录制视频线程
        threads = []
        for timestamp in timestamps:
            screenshot_thread = ScreenshotThread(package_name, timestamp, output_dir)
            record_thread = RecordThread(package_name, timestamp, output_dir)
            screenshot_thread.start()
            record_thread.start()
            threads.append(screenshot_thread)
            threads.append(record_thread)
        # 等待线程结束
        for thread in threads:
            thread.join()

    # 保存 logcat 日志和错误信息到文件
    save_logcat_and_errors(logcat_output, errors, output_dir)
