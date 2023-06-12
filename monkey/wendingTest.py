# monkey结合cpu和mem未完成
# by Shirley 2023/06/12
import os
import subprocess
import time
import threading

# 连接 adb 设备
def connect_device(device):
    if device.startswith('tcp:'):
        subprocess.call(['adb', 'disconnect'])
        subprocess.call(['adb', 'connect', device])
    else:
        subprocess.call(['adb', 'shell'])

# 执行 monkey 测试
def run_monkey(package_name, event_count):
    subprocess.call(['adb', 'shell', 'monkey', '-p', package_name, str(event_count)])

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

# 监控线程
class MonitorThread(threading.Thread):
    def __init__(self, package_name, output_dir):
        super().__init__()
        self.package_name = package_name
        self.output_dir = output_dir
        self.cpu_data = []
        self.mem_data = []
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            # 抓取 CPU 和 MEM 数据
            top_output = subprocess.check_output(['adb', 'shell', 'top', '-n', '1', '-b', '-d', '1', '-p', self.package_name]).decode()
            cpu_percent = 0
            mem_percent = 0
            for line in top_output.splitlines():
                if line.startswith(self.package_name):
                    items = line.split()
                    cpu_percent = float(items[2].rstrip('%'))
                    mem_percent = float(items[6].rstrip('%'))
                    break
            # 添加到数据列表中
            self.cpu_data.append(cpu_percent)
            self.mem_data.append(mem_percent)
            # 休眠 1 秒
            time.sleep(1)

        # 生成并保存动态监控
        self.save_monitor_data()

    def stop(self):
        self.stop_event.set()

    def save_monitor_data(self):
        # 生成 CPU 和 MEM 数据文件
        with open(os.path.join(self.output_dir, 'cpu.txt'), 'w') as f:
            f.write('\n'.join(str(x) for x in self.cpu_data))
        with open(os.path.join(self.output_dir, 'mem.txt'), 'w') as f:
            f.write('\n'.join(str(x) for x in self.mem_data))

        # 生成 CPU 和 MEM 图表
        import matplotlib.pyplot as plt
        plt.plot(self.cpu_data)
        plt.xlabel('Time (s)')
        plt.ylabel('CPU (%)')
        plt.savefig(os.path.join(self.output_dir, 'cpu.png'))
        plt.clf()
        plt.plot(self.mem_data)
        plt.xlabel('Time (s)')
        plt.ylabel('MEM (%)')
        plt.savefig(os.path.join(self.output_dir, 'mem.png'))
        plt.clf()

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
    event_count = 1000
    output_dir = 'D:/monkeylog'

    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 连接 adb 设备
    connect_device(device)
    # 执行 monkey 测试
    monkey_thread = threading.Thread(target=run_monkey, args=(package_name, event_count))
    monkey_thread.start()

    # 启动监控线程
    monitor_thread = MonitorThread(package_name, output_dir)
    monitor_thread.start()

    # 等待 monkey 测试结束
    monkey_thread.join()

    # 停止监控线程
    monitor_thread.stop()
    monitor_thread.join()

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
