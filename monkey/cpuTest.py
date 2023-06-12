# 监控手机app的qq应用CPU信息
# by Shirley 2023.06.12
import os
import time
while True:
    res = os.popen('adb shell top -n 1 -d 1 | findstr com.tencent.mobileqq').read().strip().split('\n')
    print(res)
    cpu_count = 0
    mem_count = 0
    for cpu in res:
        if cpu:
            cpu = cpu.split(' ')
            try:
                cpu_count += float(cpu[cpu.index('S')+2])
            except:
                pass
    print(cpu_count)
    time.sleep(1)