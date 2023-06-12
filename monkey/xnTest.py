
# 未完成
# by Shirley 2023.06.12
import os
import time
import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

# 获取内存信息
def get_memory_info():
    cmd = 'adb shell dumpsys meminfo com.tencent.mobileqq'
    result = os.popen(cmd).read()
    return result

# 获取CPU信息
def get_cpu_info():
    cmd = 'adb shell dumpsys cpuinfo | grep com.tencent.mobileqq'
    result = os.popen(cmd).read()
    return result

# 获取响应时间
def get_response_time():
    cmd = 'adb shell am start -W -n com.tencent.mobileqq/.activity.SplashActivity'
    os.system(cmd)
    time.sleep(5)
    cmd = "adb logcat -d | grep 'Displayed com.tencent.mobileqq/.activity.SplashActivity'"
    result = os.popen(cmd).read()
    return result

# 获取冷启动时间
def get_cold_boot_time():
    cmd = 'adb shell am start -W -n com.tencent.mobileqq/.activity.SplashActivity'
    result = os.popen(cmd).read()
    return result

# 获取热启动时间
def get_hot_boot_time():
    cmd = 'adb shell am start -W -n com.tencent.mobileqq/.activity.SplashActivity'
    os.system(cmd)
    time.sleep(5)
    cmd = 'adb shell input keyevent 3'
    os.system(cmd)
    time.sleep(5)
    cmd = 'adb shell am start -W -n com.tencent.mobileqq/.activity.SplashActivity'
    result = os.popen(cmd).read()
    return result

# 获取内存泄漏信息（比较前后内存占用）
def get_memory_leak():
    cmd1 = 'adb shell dumpsys meminfo com.tencent.mobileqq'
    time.sleep(5)
    cmd2 = 'adb shell dumpsys meminfo com.tencent.mobileqq'
    result1 = os.popen(cmd1).read()
    result2 = os.popen(cmd2).read()
    # 解析result1和result2计算内存泄漏
    return memory_leak

# 获取流畅度信息
def get_smoothness():
    cmd = 'adb shell monkey -p com.tencent.mobileqq -v 500'
    result = os.popen(cmd).read()
    # 解析result计算流畅度
    return smoothness_info

# 获取log和时间点信息
def get_log_and_timestamp():
    cmd = 'adb logcat -d -s "TAG1" "TAG2"'
    result = os.popen(cmd).read()
    # 解析result获取log和时间点
    return log_info, timestamp_info

# 生成html报告
@app.route('/')
def index():
    # 获取性能参数
    memory_info = get_memory_info()
    cpu_info = get_cpu_info()
    response_time = get_response_time()
    cold_boot_time = get_cold_boot_time()
    hot_boot_time = get_hot_boot_time()
    memory_leak = get_memory_leak()
    smoothness_info = get_smoothness()
    log_info, timestamp_info = get_log_and_timestamp()

    # 保存性能参数到csv文件
    data = {'memory': memory_info, 'cpu': cpu_info, 'response_time':response_time, 'cold_boot_time': cold_boot_time, 'hot_boot_time': hot_boot_time, 'memory_leak': memory_leak, 'smoothness': smoothness_info, 'log': log_info, 'timestamp': timestamp_info} 
    df = pd.DataFrame(data=data) 
    df.to_csv('performance_data.csv', index=False)

    # 分析性能参数
    memory_mean = df['memory'].mean()
    cpu_max = df['cpu'].max()
    response_time_mean = df['response_time'].mean()
    cold_boot_time_mean = df['cold_boot_time'].mean()
    hot_boot_time_mean = df['hot_boot_time'].mean()
    memory_leak_mean = df['memory_leak'].mean()
    smoothness_mean = df['smoothness'].mean()

    # 传递性能参数到html模板
    return render_template('performance_report.html', memory_mean=memory_mean, cpu_max=cpu_max, response_time_mean=response_time_mean, cold_boot_time_mean=cold_boot_time_mean, hot_boot_time_mean=hot_boot_time_mean, memory_leak_mean=memory_leak_mean, smoothness_mean=smoothness_mean)

