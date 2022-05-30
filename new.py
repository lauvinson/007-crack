import cv2
import numpy as np

for i in range(1, 6):
    img = cv2.imread('./jpg/' + str(i) + '.png', 0)
    re, img1 = cv2.threshold(img, 125, 255, 0)
    cv2.namedWindow('img', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('img', img1)
    contours, b = cv2.findContours(img1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    x, y = np.unravel_index(contours.argmax(), contours.shape)
    cv2.waitKey(0)
    for j in range(0, len(contours) - 1):
        M = cv2.moments(contours[j])  # 计算第⼀条轮廓的各阶矩,字典形式
        try:  # 防⽌分母等于0报错
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])
        except:
            continue  # 如果分母等于0,那⼀定不是我们的⽬标,因此可以直接跳过当前循环
        area = cv2.contourArea(contours[j])
        if area < 6000 or area > 8000 or center_x < 500:
            continue
        print(area)
        print(center_x)
        image = cv2.imread('./jpg/' + str(i) + '.png', 1)
        image = cv2.drawContours(image, contours, j, 255, 3)  # 绘制轮廓
        image = cv2.circle(image, (center_x, center_y), 7, 128, -1)  # 绘制中⼼点
        cv2.imshow('png', image)
        cv2.waitKey(0)
