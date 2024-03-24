# -*- coding: utf-8 -*-
# @Author : PuYang
# @Time   : 2023/12/24
# @File   : utils.py

import time
import cv2
import os
import yaml
import sqlite3
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMessageBox
import numpy as np
# import easyocr
import re
from datetime import datetime

class VideoHandler(QObject):
    progress_changed = pyqtSignal(float, object)
    processing_finished = pyqtSignal()
    pause_signal = pyqtSignal()
    resume_signal = pyqtSignal()

    def __init__(self, input_video_path, output_video_path, list_depth, list_frame, start_frame=0, is_superX=False, model_name="cubic_x2"):
        super().__init__()

        self.input_video_path = input_video_path
        self.output_video_path = output_video_path
        self.list_depth = list_depth
        self.list_frame = list_frame

        self.is_paused = False
        self.stop_flag = False
        self.start_frame = start_frame
        self.is_superX = is_superX
        if not model_name.endswith('.pb'):
            self.model_name = "{}.pb".format(model_name)
        else:
            self.model_name = model_name
        if self.is_superX:
            model_scale = int('{}'.format(model_name).split("_x")[-1])
            self.scale = model_scale
        else:
            self.scale = 1
        self.is_running = False

    # 视频添加水印
    def run(self):
        # 加载默认配置
        self.default_config = load_config()
        self.x = int(self.default_config['x'])
        self.y = int(self.default_config['y'])
        self.font_size = float(self.default_config['font_size'])
        self.background_color = color_to_hex(self.default_config['background_color'])
        self.font_color = color_to_hex(self.default_config['font_color'])

        # 读取视频
        cap = cv2.VideoCapture(self.input_video_path)
        zong_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        # 获取视频帧率和帧数
        fps = cap.get(cv2.CAP_PROP_FPS)
        # 设置输出视频的编解码器、帧率、大小
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        w = int(cap.get(3))
        h = int(cap.get(4))
        if self.is_superX:
            w = w * self.scale
            h = h * self.scale
            print("w:{},h:{}".format(w, h))
        out = cv2.VideoWriter(self.output_video_path, fourcc, fps, (w, h))

        previous_end_frame = 0
        for depth_t, frame_t in zip(self.list_depth, self.list_frame):
            start_depth = depth_t[0]
            end_depth = depth_t[1]
            start_frame = frame_t[0]
            end_frame = frame_t[1]

            total_frames = end_frame - start_frame

            # 添加深度信息水印到视频的每一帧
            cap.set(cv2.CAP_PROP_POS_FRAMES, previous_end_frame)

            if end_frame < self.start_frame:
                cap.set(cv2.CAP_PROP_POS_FRAMES, self.start_frame)
                continue

            while cap.isOpened():

                if self.is_paused:
                    break

                ret, frame = cap.read()
                current_frame = cap.get(cv2.CAP_PROP_POS_FRAMES)

                if not ret or current_frame >= end_frame:
                    break

                # 计算当前帧对应的深度值
                current_depth = start_depth + (end_depth - start_depth) * ((current_frame - start_frame) / total_frames)

                if self.is_superX:
                    frame = super_resolution_with_modelname(frame, self.model_name)

                # 在视频帧上添加深度信息水印
                depth_text = f"{current_depth:.3f} m"

                # 添加一个透明的黄色背景在depth_text下面
                depth_text_size = cv2.getTextSize(depth_text, cv2.FONT_HERSHEY_SIMPLEX, self.font_size, 2)[0]

                # background_color = self.background_color  # 背景 255 250 227
                # text_color = self.font_color  # 文本

                # 计算矩形的大小和位置
                rect_top_left = (self.x, self.y - 10)
                rect_bottom_right = (self.x + depth_text_size[0], self.y + depth_text_size[1] + 10)

                # 绘制填充矩形
                cv2.rectangle(frame, rect_top_left, rect_bottom_right, self.background_color, -1)

                # 绘制文本
                cv2.putText(frame, depth_text, (self.x, depth_text_size[1] + self.y), cv2.FONT_HERSHEY_SIMPLEX, self.font_size, self.font_color,
                            2, cv2.LINE_AA)

                # 写入输出视频
                out.write(frame)

                if self.stop_flag:
                    break

                if self.progress_changed:
                    process = current_frame * 100.0 / zong_frames
                    self.progress_changed.emit(process, frame)

            previous_end_frame = end_frame

        print("[INFO] video saved to {}".format(self.output_video_path))
        if self.progress_changed:
            if self.stop_flag or not self.is_paused:
                self.progress_changed.emit(100.0, None)

        self.processing_finished.emit()
        # 释放资源
        cap.release()
        out.release()


    def stop(self):
        self.stop_flag = True
        print("[INFO] video handler stopped")

    def pause(self):
        self.is_paused = True
        print("pause 时的帧数为".format(self.start_frame))
        self.pause_signal.emit()

    def resume(self):
        self.is_paused = False
        self.resume_signal.emit()
        print("resume ... ")


class Database:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS data
                              (current_frame INTEGER PRIMARY KEY, 
                              depth REAL,
                              time_info TEXT)''')
        self.conn.commit()

    def add_data(self, current_frame, depth, current_time):
        existing_depth = self.get_data_by_frame(current_frame)
        if existing_depth is not None:
            self.update_data(current_frame, depth, current_time)
        else:
            self.cursor.execute("INSERT OR REPLACE INTO data VALUES (?, ?, ?)", (current_frame, depth, current_time))
            self.conn.commit()

    def delete_data(self, current_frame):
        self.cursor.execute("DELETE FROM data WHERE current_frame=?", (current_frame,))
        self.conn.commit()

    def update_data(self, current_frame, new_depth, current_time):
        self.cursor.execute("UPDATE data SET depth=?, time_info=? WHERE current_frame=?", (new_depth, current_time, current_frame))
        self.conn.commit()

    def get_data(self):
        self.cursor.execute("SELECT * FROM data ORDER BY current_frame")
        return self.cursor.fetchall()

    def get_data_by_frame(self, current_frame):
        self.cursor.execute("SELECT depth FROM data WHERE current_frame=?", (current_frame,))
        result = self.cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None

    def close(self):
        self.conn.close()


def get_video_image(video_path, frame_num=1):

    vidcap = cv2.VideoCapture(video_path)
    # 获取帧数
    zong_count = vidcap.get(7)

    if frame_num >= zong_count:
        frame_num = zong_count-1
    print(f"frame_count = {zong_count} | last frame_num = {frame_num}")

    # 指定帧
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)

    ret, image = vidcap.read()

    if ret:
        # 将OpenCV图像格式转换为Qt图像格式
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        # 将图像转换为QPixmap
        pixmap = QPixmap.fromImage(q_image)
        return pixmap
    else:
        return

# 图像超分
def super_resolution(image):
    # 解析模型名称和缩放因子
    mn = "ESPCN_x2.pb"
    model_name = mn.split(os.path.sep)[-1].split("_")[0].lower()
    model_scale = 'model/{}'.format(mn).split("_x")[-1]
    model_scale = int(model_scale[:model_scale.find(".")])

    print("[INFO] loading super resolution model: {}".format(mn))
    print("[INFO] model name: {}".format(model_name))
    print("[INFO] model scale: {}".format(model_scale))

    # 创建超分辨率模型
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel('./model/{}'.format(mn))
    sr.setModel(model_name, model_scale)

    # 加载输入图像
    if isinstance(image, str):
        image = cv2.imread(image)

    print("[INFO] w: {}, h: {}".format(image.shape[1], image.shape[0]))

    # 进行超分辨率增强
    start = time.time()
    upscaled = sr.upsample(image)
    end = time.time()
    print("[INFO] super resolution took {:.6f} seconds".format(end - start))
    print("[INFO] w: {}, h: {}".format(upscaled.shape[1], upscaled.shape[0]))

    return upscaled

def super_resolution_with_modelname(image, mn="ESPCN_x2"):
    if not mn.endswith('.pb'):
        mn = "{}.pb".format(mn)
    # 解析模型名称和缩放因子
    model_name = mn.split(os.path.sep)[-1].split("_")[0].lower()
    model_scale = 'model/{}'.format(mn).split("_x")[-1]
    model_scale = int(model_scale[:model_scale.find(".")])

    print("[INFO] loading super resolution model: {}".format(mn))
    print("[INFO] model name: {}".format(model_name))
    print("[INFO] model scale: {}".format(model_scale))

    # 加载输入图像
    if isinstance(image, str):
        image = cv2.imread(image)

    print("[INFO] w: {}, h: {}".format(image.shape[1], image.shape[0]))

    if model_name == "cubic":
        # 使用双三次插值进行放大，作为对比
        start = time.time()
        bicubic = cv2.resize(image, (image.shape[1] * model_scale, image.shape[0] * model_scale), interpolation=cv2.INTER_CUBIC)
        end = time.time()
        print("[INFO] bicubic interpolation took {:.6f} seconds".format(end - start))

        return bicubic

    else:

        # 创建超分辨率模型
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        sr.readModel('./model/{}'.format(mn))
        sr.setModel(model_name, model_scale)

        # 进行超分辨率增强
        start = time.time()
        upscaled = sr.upsample(image)
        end = time.time()
        print("[INFO] super resolution took {:.6f} seconds".format(end - start))
        print("[INFO] w: {}, h: {}".format(upscaled.shape[1], upscaled.shape[0]))

        return upscaled

# 改变图片图片亮度和对比度
def adjust_brightness_contrast(image, brightness, contrast):
    # 将输入范围从0-100映射到调整参数的范围
    brightness = brightness / 50.0
    contrast = contrast / 50.0
    # 亮度调整
    image = cv2.convertScaleAbs(image, alpha=brightness)
    # 对比度调整
    image = np.clip((contrast * image + brightness), 0, 255).astype(np.uint8)
    return image

def show_warning_message_box(text):
    # 创建消息框
    msgBox = QMessageBox()

    # 设置消息框样式表
    msgBox.setStyleSheet("QMessageBox {background-color: white; color: black}")

    # 配置警告信息
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText(text)

    # 配置title
    msgBox.setWindowTitle("Warning")

    # 显示消息框
    msgBox.exec_()

# 十六进制转为rgb值
def hex2rgb(hex):
    return tuple(int(hex[i:i + 2], 16) for i in (0, 2, 4))

# rgb转为16进制
def rgb2hex(rgb):
    return '#%02x%02x%02x' % rgb

def color_to_hex(color_code):
    # 将16进制字符串类型的颜色值转换为整数类型的RGB值
    rgb = tuple(int(color_code[i:i + 2], 16) for i in (1, 3, 5))
    # 将RGB格式的颜色值转换为BGR格式的颜色值
    bgr = (rgb[2], rgb[1], rgb[0])
    return bgr

#读取配置文件
def load_config(config_file="res/config.yaml"):
    # 读取配置文件
    with open(config_file, 'r') as file:
        data = yaml.safe_load(file)
    return data

# 更新配置文件
def update_config(x='20', y='20', font_size='13', background_color="#4ff0ff", font_color="#000000", config_file="res/config.yaml"):
    config = {
        'x': x,
        'y': y,
        'font_size': font_size,
        'background_color': background_color,
        'font_color': font_color
    }
    print(config)
    with open(config_file, 'w') as file:
        yaml.dump(config, file)

def update_pic_preview_config(brightness=50, contrast=50, is_super_view=False, config_file="res/config_pic_prev.yaml"):
    config = {
        'brightness': brightness,
        'contrast': contrast,
        'is_super_view': is_super_view
    }
    print(config)
    with open(config_file, 'w') as file:
        yaml.dump(config, file)

# 写一个提示信息
def show_info_message_box(title="删除", msg="确定删除?"):
    # 创建消息框
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Question)
    msgBox.setWindowTitle(title)
    msgBox.setText(msg)
    msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    msgBox.setDefaultButton(QMessageBox.No)
    # 设置样式
    msgBox.setStyleSheet("background-color: white; color: black;")
    reply = msgBox.exec_()
    return reply == QMessageBox.No

# 识别图片文字
# def ocr_image(image_path_or_object):
#     # 判断 image_path_or_object 是否是已读取的图像对象
#     if isinstance(image_path_or_object, (str, bytes)):
#         # 如果是字符串或字节数组，则使用 cv2.imread 加载图像
#         image = cv2.imread(image_path_or_object)
#     else:
#         # 否则，将其视为已读取的图像对象
#         image = image_path_or_object
#
#     # 获取图像宽度和高度
#     # height, width = image.shape[:2]
#     #
#     # # 划分成四个区域（左上、左下、右下、右上）, 识别右上角
#     # right_top = image[0:height // 2, width // 2:width]
#     reader = easyocr.Reader(['ch_sim', 'en'])
#     result = reader.readtext(image)
#     # 提取识别结果
#     text_list = [res[1] for res in result]
#     return text_list

# 判断时间格式是否符合标准，类似'01:49:3?'
def extract_valid_time(time_str):
    # 使用正则表达式提取时间字符串
    match = re.search(r'\d{1,2}\s*:\s*\d{1,2}\s*:\s*\d{1,2}', time_str)
    if match:
        time_str = match.group()
        # 将时间字符串转换为datetime对象，并检查是否符合标准时间格式
        try:
            datetime.strptime(time_str, '%H:%M:%S')
        except ValueError:
            # 不符合标准时间格式
            return None
        # 返回提取到的有效时间字符串
        return time_str
    else:
        # 如果无法提取到有效的时间字符串，则剔除该数据
        return None

def is_valid_time_format(time_str):
    pattern = r'^[0-2][0-9]:[0-5][0-9]:[0-5][0-9]$'
    return bool(re.match(pattern, time_str))

# 计算两个'%H:%M:%S'的时间差
def calculate_time_difference(time1, time2):
    format_str = "%H:%M:%S"
    time_obj1 = datetime.strptime(time1, format_str)
    time_obj2 = datetime.strptime(time2, format_str)

    time_diff = abs(time_obj1 - time_obj2)
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    result = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    return result


if __name__ == '__main__':
    # 测试封装的函数
    input_video_path = 'res/input.mp4'
    output_video_path = 'res/output_video_with_depth_watermark.mp4'
    start_depth = 10.783
    end_depth = 39.456
    list_frame = [(10, 20), (20, 30), (30, 40)]
    list_depth = [(10.783, 39.456), (10.783, 39.456), (10.783, 39.456)]
    handle = VideoHandler(start_depth, end_depth, list_frame, list_depth)
    # handle.add_depth_watermark_to_video(input_video_path, output_video_path, list_depth, list_frame)