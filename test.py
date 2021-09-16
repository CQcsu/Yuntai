# -*- coding: UTF-8 -*-
from steer import Steering
import time

# 初始化steer对象
# pwm通道， 初始化位置， 最小角度， 最大角度， 步长
# steer = Steering(11, 90, 0, 180, 10)
steer = Steering(12, 90, 0, 180, 10)
time.sleep(1)

if __name__ == '__main__':
    while True:
        # 舵机正转40度
        for i in range(0, 4):
            steer.forward_rotation()
        time.sleep(1)
        # 舵机反转40度
        for i in range(0, 4):
            steer.reverse_rotation()
        time.sleep(1)





















