# 未完成
# by Shirley 2023.06.12
import os
import time
import psutil
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import subprocess

# 定义常量
PACKAGE_NAME = "com.tencent.mobileqq"
MONKEY_CMD = "adb shell monkey -p {} 1".format(PACKAGE_NAME)
LOGCAT_CMD = "adb logcat -v time -d | grep '{}\|ActivityManager'".format(PACKAGE_NAME)


# 获取CPU和内存占用率
def get_cpu_mem():
    pid = os.popen("adb shell pidof {}".format(PACKAGE_NAME)).read().strip()
    if pid:
        pid = int(pid)
        p = psutil.Process(pid)
        cpu_percent = p.cpu_percent()
        mem_percent = p.memory_percent()
        return cpu_percent, mem_percent
    else:
        return None
# 获取响应时间
def get_response_time():
    cmd = "adb shell am start -W -n {}/.activity.SplashActivity".format(PACKAGE_NAME)
    output = os.popen(cmd).read()
    for line in output.splitlines():
        if "TotalTime" in line:
            return int(line.split()[-2])
    return None


# 获取冷启动时间
def get_cold_start_time():
    cmd = "adb shell am start -W -S -n {}/.activity.SplashActivity".format(PACKAGE_NAME)
    output = os.popen(cmd).read()
    for line in output.splitlines():
        if "TotalTime" in line:
            return int(line.split()[-2])
    return None


# 获取热启动时间
def get_hot_start_time():
    cmd = "adb shell am start -W -n {}/.activity.SplashActivity".format(PACKAGE_NAME)
    output = os.popen(cmd).read()
    for line in output.splitlines():
        if "TotalTime" in line:
            return int(line.split()[-2])
    return None


# 检测内存泄漏
def detect_memory_leak():
    log = subprocess.check_output(LOGCAT_CMD, shell=True, encoding='utf-8')
    if "Suspending all threads took" in log:
        return True
    else:
        return False


# 检测流畅度
def detect_smoothness():
    log = subprocess.check_output(LOGCAT_CMD, shell=True, encoding='utf-8')
    if "Skipped" in log:
        return False
    else:
        return True

# 获取log信息
def get_log():
    log = subprocess.check_output(LOGCAT_CMD, shell=True, encoding='utf-8')
    return log


# 绘制图表
def animate(i):
    # 获取时间戳和CPU、内存占用率
    timestamp = time.time()
    cpu_mem = get_cpu_mem()
    if not cpu_mem:
        return
    cpu_percent, mem_percent = cpu_mem

    # 记录数据
    timestamps.append(timestamp)
    cpu_percents.append(cpu_percent)
    mem_percents.append(mem_percent)

    # 获取响应时间、冷启动时间和热启动时间
    response_time = get_response_time()
    cold_start_time = get_cold_start_time()
    hot_start_time = get_hot_start_time()

    # 记录数据
    response_times.append(response_time)
    cold_start_times.append(cold_start_time)
    hot_start_times.append(hot_start_time)

    # 检测内存泄漏和流畅度
    memory_leak = detect_memory_leak()
    smoothness = detect_smoothness()

    # 更新图表
    fig = make_subplots(rows=2, cols=2, subplot_titles=("CPU and Memory Usage", "Performance Metrics", "Issues"))

    fig.add_trace(
        go.Scatter(x=timestamps, y=cpu_percents, name='CPU', mode='lines'),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=timestamps, y=mem_percents, name='Memory', mode='lines'),
        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(x=timestamps, y=response_times, name='Response Time'),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=timestamps, y=cold_start_times, name='Cold Start Time'),
        row=1, col=2
    )

    fig.add_trace(
        go.Scatter(x=timestamps, y=hot_start_times, name='Hot Start Time'),
        row=1, col=2
    )

    fig.add_trace(
        go.Bar(x=['Memory Leak', 'Smoothness'], y=[int(memory_leak), int(smoothness)]),
        row=2, col=2
    )

    fig.update_layout(title='Performance Monitor', height=800)

    fig.write_html('index.html')

    # 保存数据到文件
    with open('data.txt', 'a') as f:
        f.write('{:.2f},{:.2f},{:.2f},{},{},{}\n'.format(timestamp, cpu_percent, mem_percent, response_time, cold_start_time, hot_start_time))

    # # 更新图表
    # plt.cla()
    # plt.plot(timestamps, cpu_percents, label='CPU')
    # plt.plot(timestamps, mem_percents, label='Memory')
    # plt.legend()
    # plt.xlabel('Time')
    # plt.ylabel('Percentage')
    # plt.title('CPU and Memory Usage')

    # # 装饰
    # plt.subplot(2, 2, 2)
    # plt.plot(timestamps, response_times, label='Response Time')
    # plt.plot(timestamps, cold_start_times, label='Cold Start Time')
    # plt.plot(timestamps, hot_start_times, label='Hot Start Time')
    # plt.legend()
    # plt.xlabel('Time')
    # plt.ylabel('Milliseconds')
    # plt.title('Performance Metrics')

    # plt.subplot(2, 2, 3)
    # plt.bar(['Memory Leak', 'Smoothness'], [detect_memory_leak(), detect_smoothness()])
    # plt.title('Issues')

    # # 保存数据到文件
    # with open('data.txt', 'a') as f:
    #     # f.write('{:.2f},{:.2f},{:.2f}\n'.format(timestamp, cpu_percent, mem_percent))
    #     f.write('{:.2f},{:.2f},{:.2f},{},{},{}\n'.format(timestamp, cpu_percent, mem_percent, response_time, cold_start_time, hot_start_time))


# 执行monkey测试
os.system(MONKEY_CMD)

# 初始化数据
timestamps = []
cpu_percents = []
mem_percents = []
response_times = [] 
cold_start_times = [] 
hot_start_times = []
# 绘制初始图表
# fig = plt.figure()
fig = plt.figure(figsize=(10, 8)) 
ani = FuncAnimation(fig, animate, interval=1000)


# 生成HTML页面
html_template = """
<html>
<head>
    <title>Performance Monitor</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <h1>Performance Monitor</h1>
    <div id="plot"></div>
    <script>
        var data = [
            {{
                x: {timestamps},
                y: {cpu_percents},
                name: 'CPU',
                mode: 'lines'
            }},
            {{
                x: {timestamps},
                y: {mem_percents},
                name: 'Memory',
                mode: 'lines'
            }}
        ];
        var layout = {{
            title: 'Performance Monitor',
            xaxis: {{
                title: 'Time'
            }},
            yaxis: {{
                title: 'Percentage'
            }}
        }};
        Plotly.newPlot('plot', data, layout);
    </script>
</body>
</html>
""".format(timestamps=timestamps, cpu_percents=cpu_percents, mem_percents=mem_percents)
with open('index.html', 'w') as f:
    f.write(html_template)

# 输出log信息
log = get_log()
print(log)
