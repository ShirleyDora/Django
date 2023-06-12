# 简单cpu和mem的demo,byShirley 20230612
import subprocess
import psutil
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from appium import webdriver

# 连接到手机上的 QQ 应用
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '10'
desired_caps['deviceName'] = 'xxx'
desired_caps['appPackage'] = 'com.tencent.mobileqq'
desired_caps['appActivity'] = '.activity.SplashActivity'

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

# 获取 QQ 应用的进程 ID
output = subprocess.check_output(['adb', 'shell', 'pidof', 'com.tencent.mobileqq'])
pid = int(output.strip())

# 绘制实时的 CPU 和内存占用情况
fig, ax = plt.subplots(2, 1)

def update(frame):
    # 获取 CPU 和内存占用情况
    process = psutil.Process(pid)
    cpu_percent = process.cpu_percent()
    memory_percent = process.memory_percent()

    # 更新图表
    ax[0].cla()
    ax[0].set_ylim(0, 100)
    ax[0].set_title('CPU Usage')
    ax[0].bar('', cpu_percent)
    ax[1].cla()
    ax[1].set_ylim(0, 100)
    ax[1].set_title('Memory Usage')
    ax[1].bar('', memory_percent)

ani = animation.FuncAnimation(fig, update, interval=1000)
plt.show()

# 关闭连接
driver.quit()
