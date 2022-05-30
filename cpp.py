#!/usr/bin/env python
# encoding: utf-8

# -*- coding: utf-8 -*-
# @contact: ybsdeyx@foxmail.com
# @software: PyCharm
# @time: 2019/4/25 16:39
# @author: Paulson●Wier
# @file: captcha_qq.py
# @desc:
import base64
import re
from io import BytesIO

import numpy as np
import random

import requests
from selenium.webdriver import ActionChains
import time
from selenium import webdriver
from PIL import Image
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import cv2


def base64_to_image(base64_str):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    return img


slideBgJs = "let c = document.createElement('canvas');let ctx = c.getContext('2d');" \
     "let img = document.getElementById('slideBg'); /*找到图片*/ " \
     "c.height=img.naturalHeight;c.width=img.naturalWidth;" \
     "ctx.drawImage(img, 0, 0,img.naturalWidth, img.naturalHeight);" \
     "let base64String = c.toDataURL();return base64String;"

slideBlockJs = "let c = document.createElement('canvas');let ctx = c.getContext('2d');" \
     "let img = document.getElementById('slideBlock'); /*找到图片*/ " \
     "c.height=img.naturalHeight;c.width=img.naturalWidth;" \
     "ctx.drawImage(img, 0, 0,img.naturalWidth, img.naturalHeight);" \
     "let base64String = c.toDataURL();return base64String;"


class Login(object):
    """
    腾讯防水墙滑动验证码破解
    使用OpenCV库
    成功率大概90%左右：在实际应用中，登录后可判断当前页面是否有登录成功才会出现的信息：比如用户名等。循环
    https://007.qq.com
    破解 腾讯滑动验证码
    腾讯防水墙
    python + seleniuum + cv2
    """
    def __init__(self):
        # 如果是实际应用中，可在此处账号和密码
        self.url = "https://007.qq.com"
        self.driver = webdriver.Chrome()

    @staticmethod
    def show(name):
        cv2.imshow('Show', name)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def webdriverwait_send_keys(dri, element, value):
        """
        显示等待输入
        :param dri: driver
        :param element:
        :param value:
        :return:
        """
        WebDriverWait(dri, 10, 5).until(lambda dr: element).send_keys(value)

    @staticmethod
    def webdriverwait_click(dri, element):
        """
        显示等待 click
        :param dri: driver
        :param element:
        :return:
        """
        WebDriverWait(dri, 10, 5).until(lambda dr: element).click()

    @staticmethod
    def get_postion(chunk, canves):
        img = cv2.imread(chunk, 0)
        re, img1 = cv2.threshold(img, 125, 255, 0)
        contours, b = cv2.findContours(img1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        for j in range(0, len(contours) - 1):
            M = cv2.moments(contours[j])  # 计算第一条轮廓的各阶矩,字典形式
            try:
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
            except:
                continue
            area = cv2.contourArea(contours[j])
            if area < 6000 or area > 8000 or center_x < 500:
                continue
            return center_x
        """
        判断缺口位置
        :param chunk: 缺口图片是原图
        :param canves:
        :return: 位置 x, y
        """
        # otemp = chunk
        # oblk = canves
        # target = cv2.imread(otemp, 0)
        # template = cv2.imread(oblk, 0)
        # # w, h = target.shape[::-1]
        # temp = 'temp.jpg'
        # targ = 'targ.jpg'
        # cv2.imwrite(temp, template)
        # cv2.imwrite(targ, target)
        # target = cv2.imread(targ)
        # target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        # target = abs(255 - target)
        # cv2.imwrite(targ, target)
        # target = cv2.imread(targ)
        # template = cv2.imread(temp)
        # result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        # x, y = np.unravel_index(result.argmax(), result.shape)
        # # # # 展示圈出来的区域
        # # # cv2.circle(target, (x, y), 7, 128, -1)  # 绘制中⼼点
        # # # cv2.imwrite("yuantu.jpg", target)
        # # # show(template)
        # return x, y

    @staticmethod
    def get_track(distance):
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.15
        # 初速度
        v = 1
        r = [0.9, 0.95, 0.975, 1, 1.025, 1.05, 1.1]
        i = 0
        while current < distance:
            if current < mid:
                a = 1
            else:
                a = -3.5
            v0 = v
            v = v0 + a * t
            r1 = random.choice(r)
            move = v * t * r1
            current += move
            track.append(move)
            if distance - current <= move:
                track.append(distance - current)
                return track
            i = i + 1
        return track

    @staticmethod
    def urllib_download(imgurl, imgsavepath):
        """
        下载图片
        :param imgurl: 图片url
        :param imgsavepath: 存放地址
        :return:
        """
        from urllib.request import urlretrieve
        urlretrieve(imgurl, imgsavepath)

    def after_quit(self):
        """
        关闭浏览器
        :return:
        """
        self.driver.quit()

    def login_main(self):
        # ssl._create_default_https_context = ssl._create_unverified_context
        driver = self.driver
        # driver.minimize_window()
        driver.get(self.url)
        self.wait = WebDriverWait(self.driver, 10)

        click_keyi_username = driver.find_element_by_xpath("//div[@class='wp-onb-tit']/a[text()='体验用户']")
        self.webdriverwait_click(driver, click_keyi_username)

        login_button = driver.find_element_by_id('code')
        self.webdriverwait_click(driver, login_button)

        self.wait.until(expected_conditions.presence_of_element_located((By.ID, 'tcaptcha_iframe')))
        driver.switch_to.frame(driver.find_element_by_id('tcaptcha_iframe'))  # switch 到 滑块frame
        bk_block = self.wait.until(
                expected_conditions.presence_of_element_located((By.XPATH, '//div/img[@id="slideBg"]')))  # 大图
        web_image_width = bk_block.size
        web_image_width = web_image_width['width']
        bk_block_x = bk_block.location['x']

        slide_block = driver.find_element_by_xpath('//img[@id="slideBlock"]')  # 小滑块
        slide_block_x = slide_block.location['x']

        # bk_block = driver.find_element_by_xpath('//img[@id="slideBg"]').get_attribute('src')       # 大图 url
        # slide_block = driver.find_element_by_xpath('//img[@id="slideBlock"]').get_attribute('src')  # 小滑块 图片url

        os.makedirs('./image/', exist_ok=True)
        # self.urllib_download(bk_block, './image/bkBlock.png')
        # self.urllib_download(slide_block, './image/slideBlock.png')
        base64_to_image(driver.execute_script(slideBgJs)).save('./image/bkBlock.png')
        base64_to_image(driver.execute_script(slideBlockJs)).save('./image/slideBlock.png')
        # time.sleep(0.5)
        img_bkblock = Image.open('./image/bkBlock.png')
        real_width = img_bkblock.size[0]
        width_scale = float(real_width) / float(web_image_width)
        position = self.get_postion('./image/bkBlock.png', './image/slideBlock.png')
        if position is None:
            return
        real_position = position - 119.194
        real_position = real_position / 1.72
        real_position = real_position - (slide_block_x - bk_block_x)
        track_list = self.get_track(real_position)

        print('滑动轨迹:', int(real_position), track_list)
        # print('第一步,获取滑动按钮')
        slid_ing = self.wait.until(
            expected_conditions.presence_of_element_located((By.XPATH, '//div[@class="tc-drag-thumb"]')))
        ActionChains(driver).click_and_hold(on_element=slid_ing).perform()  # 点击鼠标左键，按住不放
        # print('第二步,拖动元素')
        for track in track_list:
            ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()  # 鼠标移动到距离当前位置（x,y）
            # time.sleep(0.002)
        # ActionChains(driver).move_by_offset(xoffset=-random.randint(0, 1), yoffset=0).perform()   # 微调，根据实际情况微调
        time.sleep(1)
        # print('第三步,释放鼠标')
        ActionChains(driver).release(on_element=slid_ing).perform()
        time.sleep(1)


if __name__ == '__main__':
    phone = "****"
    login = Login()
    for i in range (10):
        login.login_main()
