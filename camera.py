# -*- coding: UTF-8 -*-
# 摄像头实现红球捕捉 将像素信息提供给舵机 实现目标跟踪
import cv2
import numpy as np
import math


class Camera:
    # 摄像头相关参数设置
    Lower_red_1 = np.array([0, 160, 140])
    Upper_red_1 = np.array([10, 255, 255])
    Lower_red_2 = np.array([155, 160, 140])
    Upper_red_2 = np.array([179, 255, 255])
    BLACK = [0, 0, 0]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    detect_threshold = 0.0015

    def find_red_ball(self, frame):
        img = cv2.flip(frame, 1)  # 视频显示左右翻转
        out = img.copy()
        img_area = img.shape[0] * img.shape[1]
        img_blur = cv2.GaussianBlur(img, (5, 5), 0)
        img_hsv = cv2.cvtColor(img_blur, cv2.COLOR_BGR2HSV)
        img_mask_low = cv2.inRange(img_hsv, self.Lower_red_1, self.Upper_red_1)  # 构建低集合红色掩模
        img_mask_upper = cv2.inRange(img_hsv, self.Lower_red_2, self.Upper_red_2)  # 构建高集合红色掩模
        mask = cv2.addWeighted(img_mask_low, 1.0, img_mask_upper, 1.0, 0.0)  # 融合红色掩模
        # cv2.imshow("mask", mask)
        # cv2.waitKey(5)

        img_dilate = cv2.dilate(mask, self.kernel, iterations=1)
        img_erode = cv2.erode(img_dilate, self.kernel, iterations=1)
        img_border = cv2.copyMakeBorder(img_erode, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=self.BLACK)
        img_canny = cv2.Canny(img_border, 0, 250)
        img_canny_dilate = cv2.dilate(img_canny, self.kernel, iterations=1)

        max_cnt_area = -1
        max_cnt_index = -1
        max_cnt_x, max_cnt_y, max_cnt_w, max_cnt_h = -1, -1, -1, -1
        left_right, up_down = -1, -1

        contours, hierarchy = cv2.findContours(img_canny_dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        for i, cnt in enumerate(contours):
            # 轮廓信息提取
            area = cv2.contourArea(cnt)
            x, y, w, h = cv2.boundingRect(cnt)
            if area > max_cnt_area:
                max_cnt_area = area
                max_cnt_index = i
                max_cnt_x, max_cnt_y, max_cnt_w, max_cnt_h = x, y, w, h
        if max_cnt_index != -1:
            cv2.drawContours(out, contours[max_cnt_index], -1, (255, 0, 0), 3)
        cv2.imshow("out", out)
        cv2.waitKey(5)

        cx, cy = max_cnt_y + max_cnt_h // 2, max_cnt_x + max_cnt_w // 2
        if max_cnt_area / img_area > self.detect_threshold:
            if cy <= 320:
                distance_y = math.fabs(320 - cy)
                left_right = 0
                # print("左方距离中心：", distance_y)
            elif (cy > 320) and (cy <= 640):
                distance_y = math.fabs(320 - cy)
                left_right = 1
                # print("右方距离中心：", distance_y)
            if cx <= 240:
                distance_x = math.fabs(240 - cx)
                up_down = 0
                # print("上方距离中心：", distance_x)
            elif (cx >= 240) and (cx <= 480):
                distance_x = math.fabs(240 - cx)
                up_down = 1
                # print("下方距离中心：", distance_x)
            return [left_right, distance_y, up_down, distance_x]
























