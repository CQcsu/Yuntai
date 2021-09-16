# -*- coding: UTF-8 -*-
# 舵机代码和opencv代码分离， 按照对象的方式封装
# 两个舵机实现摄像头水平反向和垂直方向移动
import RPi.GPIO as GPIO
import time

# 舵机控制 ， 正转， 反转， 初始化 共三种方法


class Steering:
    max_delay = 0.20
    min_delay = 0.10

    def __init__(self, channel, init_position, min_angle, max_angle, speed):
        self.channel = channel
        self.init_position = init_position
        self.position = init_position
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.speed = speed  # 舵机正转步长

        GPIO.setmode(GPIO.BOARD)  # 设置IO口编码方式
        GPIO.setwarnings(False)  # 禁用警告, 引脚被设置为非默认值
        GPIO.setup(self.channel, GPIO.OUT)  # 设置pwm输出通道

        self.pwm = GPIO.PWM(self.channel, 50)
        self.pwm.start(2.5 + 10*self.init_position/270.0)  # 让舵机转到初始位置
        time.sleep(Steering.max_delay)

    def forward_rotation(self):
        # print("当前位置：" + str(self.position))
        if (self.position + self.speed) <= self.max_angle:
            self.position = self.position + self.speed
            self.pwm.ChangeDutyCycle(2.5 + 10*self.position/270.0)  # 设置舵机角度
            time.sleep(Steering.max_delay)
        print("正转后位置：" + str(self.position))

    def reverse_rotation(self):
        # print("当前位置：" + str(self.position))
        if (self.position - self.speed) >= self.min_angle:
            self.position = self.position - self.speed
            self.pwm.ChangeDutyCycle(2.5 + 10*self.position/270.0)  # 设置舵机角度
            time.sleep(Steering.max_delay)
        print("反转后的位置: " + str(self.position))
    
    def keep_position(self):
        self.pwm.ChangeDutyCycle(2.5 + 10*self.position/270.0)
        time.sleep(Steering.min_delay)

    def reset(self):
        print("当前位置：" + str(self.position))
        self.position = self.init_position
        self.pwm.ChangeDutyCycle(2.5 + 10*self.init_position/270)  # 让舵机转到初始位置
        time.sleep(Steering.max_delay)
        print("初始化后的位置: " + str(self.position))























