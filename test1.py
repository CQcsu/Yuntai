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
                continue
            else:
                if img_info[0] == 0:
                    print("左")
                elif img_info[0] == 1:
                    print("右")
