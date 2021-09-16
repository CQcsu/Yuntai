# -*- coding: UTF-8 -*-
from camera import Camera
from steer import Steering
import cv2
import time


# 打开摄像头 设置摄像头分辨率640*480
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 初始化摄像头对象
camera = Camera()

# 初始化steer对象
# pwm通道， 初始化位置， 最小角度， 最大角度， 步长
steer_11 = Steering(11, 90, 0, 180, 2)
steer_12 = Steering(12, 90, 40, 140, 2)
time.sleep(1)

if __name__ == '__main__':
    while True:
        ret, src = cap.read()
        if ret is False:
            print("图片读取失败")
            break
        else:
            img_info = camera.find_red_ball(src)
            # print(img_info)
            if img_info is None:
                steer_11.keep_position()
                steer_12.keep_position()
                continue
            else:
                if img_info[0] == 0:
                    if img_info[1] >= 20:  # 红球在左边， 舵机反转
                        steer_11.reverse_rotation()
                elif img_info[0] == 1:
                    if img_info[1] >= 20:  # 红球在右边， 舵机正转
                        steer_11.forward_rotation()
                if img_info[2] == 0:
                    if img_info[3] >= 20:  # 红球在上边向上转(正转)
                        steer_12.forward_rotation()
                elif img_info[2] == 1:
                    if img_info[3] >= 20:  # 红球在下边向下转(反转)
                        steer_12.reverse_rotation()








