import os
import sys
from mainWindow import Ui_mainWindow
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia
from utils import *
import pandas as pd
from collections import deque
from enum import Enum


class VideoOperation(Enum):
    Select = 1
    Process = 2

watermark_save_path = 'deepth/watermark.txt'


class Modifier(Ui_mainWindow):
    def __init__(self):
        super().__init__()
        self.index_video = 0
        self.index_picture = 0
        self.selected_video_path = ''
        self.selected_pic_path = ''
        self.selected_video_item = None
        self.selected_pic_item = None
        self.x_speed = 1
        self.jie_gu_count = 0
        # 当前选中视频的总帧数
        self.cur_total_frames = 0
        # 当前选中的视频
        self.current_video = None
        # 当前项目路径
        self.save_path = os.getcwd()
        # 创建一个定时器
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_informations)
        # 给从头开始预览给一个定时器
        self.timer1 = QtCore.QTimer()
        self.timer1.timeout.connect(self.update_preview_progress_bar)
        self.current_scatch = 1   # 当前图片播放的接箍
        self.current_item_data = None  # 当前选中视频的json数据

        # videohandler
        self.video_handler_thread = QtCore.QThread()
        self.video_handler = None

        # 是否全部开始
        self.is_all_start = False

        # 默认配置
        self.default_settings = None
        self.default_pic_settings = None

        # 全部开始，顺序执行队列
        self.video_operations = deque()
        self.current_operation = None

    # 在这个类中，修改mainwindow的属性或添加其他功能
    def modify_frame(self):
        # 设置默认显示第一个tab
        self.tabWidget.setCurrentIndex(0)

        # addbutton添加点击事件,功能为打开文件对话框
        self.addButton.clicked.connect(self.add_file)

        # deletebutton删除点击事件
        self.deleteButton.clicked.connect(self.delete_file)

        # clearbutton清空事件
        self.clearButton.clicked.connect(self.clear_file)

        # 当选中 self.video_tree_widget的item时
        self.video_tree_widget.itemClicked.connect(self.video_widget_item_selected)

        # 当选中 self.treeWidget_5的item时
        self.treeWidget_5.itemClicked.connect(self.jiegu_widget_item_selected)

        # 当双击 self.treeWidget_5的item时
        self.treeWidget_5.itemDoubleClicked.connect(self.jiegu_widget_item_double_click)

        # 设置picture_label和video_label显示图像为填充并拉伸
        self.picture_label.setScaledContents(True)

        # self.pushButton_10 添加点击事件,播放视频或者停止视频
        self.pushButton_10.clicked.connect(self.playOrStop)

        # self.pushButton_11 添加点击事件,视频暂停或者继续
        self.pushButton_11.clicked.connect(self.pauseOrContinue)

        # self.pushButton_12 添加点击事件,视频播放步进
        self.pushButton_12.clicked.connect(self.forwardSlider)

        # self.pushButton_13 添加点击事件,视频播放步退
        self.pushButton_13.clicked.connect(self.backSlider)

        # self.pushButton_14 添加点击事件, 视频倒放
        self.pushButton_14.clicked.connect(self.reversePlayback)

        # self.pushButton_15 添加点击事件, 对当前帧进行截图并保存,保存的目录由用户决定
        self.pushButton_15.clicked.connect(self.takeScreenshot)

        # self.pushButton_16 添加点击事件, 对帧添加深度信息
        self.pushButton_16.clicked.connect(self.add_depth_to_frame)

        # self.pushButton_7 添加点击事件, 选择文件夹
        self.pushButton_7.clicked.connect(self.select_folder)

        # 开始/停止处理视频
        self.pushButton_8.clicked.connect(self.start_handle_video)

        # 暂停/继续处理视频
        self.pushButton_9.clicked.connect(self.pause_handle_video)

        # 跳转到指定帧
        self.pushButton_17.clicked.connect(self.jump_to_frame)

        # 预览部分查找
        self.pushButton_18.clicked.connect(self.find_jump_to_frame)

        # 预览暂停或继续
        self.pushButton_19.clicked.connect(self.preview_start_or_pause)

        # 从头开始预览接箍
        self.pushButton_20.clicked.connect(self.start_preview_scratch)

        # 删除选中行
        self.pushButton_2.clicked.connect(self.delete_seleted_row)

        # 重新排序
        self.pushButton.clicked.connect(self.sort_picture_items)

        # 导出为excel
        self.pushButton_3.clicked.connect(self.export_to_excel)

        # 更新 self.check_box3 的状态，检测是否符合可点击的状态
        self.checkBox_3.clicked.connect(self.update_state_of_start)

        # 更新背景颜色
        self.pushButton_6.clicked.connect(self.update_background_color)

        # 更新字体颜色
        self.pushButton_23.clicked.connect(self.update_font_color)

        # 设置-确定
        self.pushButton_5.clicked.connect(self.update_settings)

        # 设置-重置
        self.pushButton_4.clicked.connect(self.reset_settings)

        # 保存pic配置
        self.pushButton_21.clicked.connect(self.update_pic_preview_settings)

        # 连接QSlider的valueChanged信号到槽函数onSliderValueChanged
        self.horizontalSlider.sliderReleased.connect(self.onBrightnessSliderValueChanged)
        self.horizontalSlider_2.sliderReleased.connect(self.onContrastSliderValueChanged)

        # 给 self.spinBox 的最大倍速为3,最小为1,默认为1
        self.spinBox.setValue(1)  # 设置默认值为1
        self.spinBox.setMinimum(1)  # 设置最小值为1
        self.spinBox.setMaximum(3)  # 设置最大值为3
        self.spinBox.valueChanged.connect(self.printSpinBoxValue)

        # 设置qtreewidget的列宽和标题宽度一致
        self.video_tree_widget.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.treeWidget_5.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.load_defaults_settings()

    # 当亮度更新时
    def onBrightnessSliderValueChanged(self):
        if len(self.selected_video_path) != 0:
            _, position = self.player.getCurrentProgress()
            self.display_frame(self.selected_video_path, position, self.picture_label)

    # 当对比度更新时
    def onContrastSliderValueChanged(self):
        if len(self.selected_video_path) != 0:
            _, position = self.player.getCurrentProgress()
            self.display_frame(self.selected_video_path, position, self.picture_label)

    # 加载默认配置
    def load_defaults_settings(self):
        # 加载配置文件内容
        self.default_settings = load_config()
        self.lineEdit_8.setText(self.default_settings["x"])
        self.lineEdit_9.setText(self.default_settings["y"])
        self.lineEdit_6.setText(self.default_settings["font_size"])
        self.label_35.setProperty("text", "{}".format(self.default_settings["background_color"]))
        # 将label_35的背景颜色设置为默认颜色
        self.label_35.setStyleSheet("background-color: {};".format(self.default_settings["background_color"]))
        self.label_36.setProperty("text", "{}".format(self.default_settings["font_color"]))
        # 将label_36的字体颜色设置为默认颜色
        self.label_36.setStyleSheet("background-color: {};".format(self.default_settings["font_color"]))
        # 加载图片预览配置
        self.default_pic_settings = load_config("res/config_pic_prev.yaml")
        print(self.default_pic_settings)
        self.horizontalSlider.setValue(self.default_pic_settings["brightness"])
        self.horizontalSlider_2.setValue(self.default_pic_settings["contrast"])
        self.checkBox_2.setChecked(self.default_pic_settings["is_super_view"])


    def update_background_color(self):
        # 调起颜色选择对话框
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            # 将颜色转化为十六进制 #******
            color = color.name(QtGui.QColor.HexRgb)
            self.label_35.setProperty("text", "{}".format(color))
            self.label_35.setStyleSheet("background-color: {};".format(color))

    def update_font_color(self):
        # 调起颜色选择对话框
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            # 将颜色转化为十六进制 #******
            color = color.name(QtGui.QColor.HexRgb)
            self.label_36.setProperty("text", "{}".format(color))
            self.label_36.setStyleSheet("background-color: {};".format(color))

    def update_settings(self):
        if show_info_message_box("设置", "确定更新设置？"):
            return

        x = self.lineEdit_8.text()
        if x == "":
            x = '20'

        y = self.lineEdit_9.text()
        if y == "":
            y = '20'

        font = self.lineEdit_6.text()
        if font == "":
            font = '1.3'

        bgcolor = self.label_35.text()
        fontcolor = self.label_36.text()

        update_config(x, y, font, bgcolor, fontcolor)

        # 展示预览图
        _, position = self.player.getCurrentProgress()
        # 将帧图像转换为QPixmap并显示在QLabel上
        self.display_frame(self.selected_video_path, position, self.picture_label)

    def reset_settings(self):
        if show_info_message_box("重置", "确定重置？"):
            return
        update_config()
        self.load_defaults_settings()
        # 展示预览图
        _, position = self.player.getCurrentProgress()
        # 将帧图像转换为QPixmap并显示在QLabel上
        self.display_frame(self.selected_video_path, position, self.picture_label)

    def update_pic_preview_settings(self):
        if show_info_message_box("保存配置", "确定保存配置？"):
            return
        config_path = "res/config_pic_prev.yaml"
        brightness = self.horizontalSlider.value()
        contrast = self.horizontalSlider_2.value()
        is_superX = self.checkBox_2.isChecked()
        update_pic_preview_config(brightness, contrast, is_superX, config_path)

    def update_state_of_start(self):

        self.is_all_start = True
        if self.video_tree_widget.topLevelItemCount() == 0:
            self.is_all_start = False
            self.checkBox_3.setChecked(False)
            show_warning_message_box("没有添加视频，请添加")
            return

        # 检测self.video_tree_widget中展示的所有视频列表,并打印出视频列表中是否有视频没有深度信息
        for i in range(self.video_tree_widget.topLevelItemCount()):
            item = self.video_tree_widget.topLevelItem(i)
            video_path = item.text(1)
            db_path = "deepth/" + video_path.split("/")[-1].split(".")[0] + ".db"
            print(db_path)
            if not os.path.exists(db_path):
                self.is_all_start = False
                self.checkBox_3.setChecked(False)
                show_warning_message_box("视频" + video_path + "没有深度信息，请先标注深度信息！")
                break

    def start_preview_scratch(self):
        sep_time = 3
        if len(self.spinBox_3.text()) > 0:
            sep_time = int(self.spinBox_3.text())
        self.current_scatch = 0

        if self.timer1.isActive():
            self.timer1.stop()
            time.sleep(0.1)

        self.timer1.start(sep_time * 1000)

    def update_preview_progress_bar(self):
        idx = self.current_scatch  # idx 序号

        if self.current_scatch > len(self.current_item_data):
            self.timer1.stop()
            self.current_scatch = 1
            print("mer1 stop,,,,,,")
        else:
            item = self.current_item_data[self.current_scatch-1]
            idx_frame = int(item[0])  # 帧号
            frame_depth = float(item[1])  # 帧对应的深度

            info = "当前接箍号{} 深度 {}M".format(idx, frame_depth)
            self.label_28.setProperty("text", info)

            total_jiegu = len(self.current_item_data)
            info1 = "当前接箍编号 {} 接箍总数 {}".format(idx, total_jiegu)
            self.label_31.setProperty("text", info1)

            qimage = get_video_image(self.selected_video_path, frame_num=idx_frame)

            self.picture_label.setPixmap(qimage)

            process = int(idx * 100 / len(self.current_item_data))
            self.progressBar_2.setValue(process)

        self.current_scatch += 1

    def preview_start_or_pause(self):
        sep_time = 3
        if len(self.spinBox_3.text()) > 0:
            sep_time = int(self.spinBox_3.text())

        if self.timer1.isActive():
            self.timer1.stop()
        else:
            self.timer1.start(sep_time * 1000)

    def jump_to_frame(self):
        if len(self.selected_video_path) == 0:
            return
        cur_frame = int(self.lineEdit.text())
        total_frame = self.cur_total_frames
        position = cur_frame * 100 * 1000 / total_frame
        self.player.mediaPlayer.setPosition(int(position))
        self.player.mediaPlayer.pause()
        self.timer.stop()

        # 将帧图像转换为QPixmap并显示在QLabel上
        self.display_frame(self.selected_video_path, cur_frame, self.picture_label)
        self.label_16.setProperty("text", "当前播放帧号 {} 总帧数 {}".format(cur_frame, self.cur_total_frames))

    def find_jump_to_frame(self):
        # 用户填写的接箍号
        usr_idx = int(self.lineEdit_2.text())
        if len(self.selected_video_path) == 0 or usr_idx > len(self.current_item_data) or usr_idx < 1:
            return
        item = self.current_item_data[usr_idx-1]
        cur_frame = int(item[0])  # 帧号
        total_frame = self.cur_total_frames
        position = cur_frame * 100 * 1000 / total_frame
        self.player.mediaPlayer.setPosition(int(position))
        self.player.mediaPlayer.pause()
        self.timer.stop()

        # 将帧图像转换为QPixmap并显示在QLabel上
        self.display_frame(self.selected_video_path, cur_frame, self.picture_label)

        self.label_16.setProperty("text", "当前播放帧号 {} 总帧数 {}".format(cur_frame, self.cur_total_frames))

        msg = "当前接箍号{},深度{}M".format(cur_frame, item[1])
        self.label_28.setProperty("text", msg)

        msg1 = "当前接箍编号 {} 接箍总数 {}".format(usr_idx, len(self.current_item_data))

        self.label_31.setProperty("text", msg1)

    def printSpinBoxValue(self, value):
        self.x_speed = value
        print("X speed:", value)
        # 设置视频播放倍速
        if self.player is not None:
            self.player.mediaPlayer.setPlaybackRate(value)

    def dragMoveEvent(self, event):
        print('move')

    def dragEnterEvent(self, event):
        print('enter')
        if event.mimeData().hasUrls():
            print("has urls")
            event.acceptProposedAction()

    def dropEvent(self, event):
        print("drag")
        # files = event.mimeData().urls()
        # for file in files:
        #     file_path = file.toLocalFile()
        #     if os.path.isfile(file_path):
        #         item = QtWidgets.QTreeWidgetItem(self.treeWidget)
        #         item.setText(0, os.path.basename(file_path))
        #     elif os.path.isdir(file_path):
        #         folder_name = os.path.basename(file_path)
        #         folder_item = QtWidgets.QTreeWidgetItem(self.treeWidget)
        #         folder_item.setText(0, folder_name)
        #         self.loadVideoFiles(file_path, folder_item)

    def loadVideoFiles(self, folder_path, parent_item):
        video_extensions = [".mp4", ".avi", ".mkv", ".mpg", ".mov", ".flv", ".mpeg"]  # 视频文件扩展名
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if os.path.splitext(file)[1].lower() in video_extensions:
                    file_item = QtWidgets.QTreeWidgetItem(parent_item)
                    file_item.setText(0, file)

    def add_file(self):

        file_names, _ = QtWidgets.QFileDialog.getOpenFileNames(window, "打开文件", "./", "视频文件(*.mp4 *.MP4)")

        # 如果没有打开视频文件
        if not file_names:
            return

        for video_path in file_names:

            # 文件名称
            video_name = video_path.split('/')[-1]
            # 计算video文件的大小
            video_size = os.path.getsize(video_path) / 1024 / 1024

            if video_size > 1024:
                video_size = video_size / 1024
                video_size = round(video_size, 2)
                video_size = str(video_size) + "GB"
            else:
                video_size = int(video_size)
                video_size = str(video_size) + "MB"
            # 将index_picture, pic_name, pic_size, pic_path添加到video_tree_widget中
            self.video_tree_widget.addTopLevelItem(
                QtWidgets.QTreeWidgetItem([str(self.index_video), video_name, video_size, video_path]))
            self.index_video += 1
            #self.video_label.setPixmap(QtGui.QPixmap(file_name[0]))

    def delete_file(self):

        if show_info_message_box():
            return

        selected_items = self.video_tree_widget.selectedItems()

        if not selected_items:
            #self.video_tree_widget.clear()
            return

        for item in selected_items:
            parent = item.parent()
            if parent is None:
                # 顶级项目
                index = self.video_tree_widget.indexOfTopLevelItem(item)
                self.video_tree_widget.takeTopLevelItem(index)
            else:
                # 子级项目
                parent.takeChild(parent.indexOfChild(item))

        # 清空列表
        self.treeWidget_5.clear()
        self.label_3.setProperty("text", "列表中选中的文件名称")

    def clear_file(self):
        if show_info_message_box("清空", "确认清空？"):
            return

        self.video_tree_widget.clear()
        self.index_video = 0

        self.player.mediaPlayer.stop()
        self.treeWidget_5.clear()
        self.picture_label.clear()
        self.label_3.setProperty("text", "列表中选中的文件名称")

    def video_widget_item_selected(self):
        selected_items = self.video_tree_widget.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            video_path = item.text(3)
            self.selected_video_item = item
            self.selected_video_path = video_path
            print('视频路径:', self.selected_video_path)

            # 根据selected_video_path, 获取视频的总帧数
            total_frame = int(cv2.VideoCapture(video_path).get(cv2.CAP_PROP_FRAME_COUNT))
            self.cur_total_frames = total_frame
            video_name = video_path.split('/')[-1].split('.')[0]
            self.current_video = video_name

            # 根据video_path将视频文件的第一帧展示在self.video_label上
            self.player.loadFilm(video_path)
            self.player.mediaPlayer.pause()

            # 存储db
            db_path = "deepth/" + self.current_video + ".db"
            # 如果没有该目录，创建该目录
            if not os.path.exists("deepth"):
                os.makedirs("deepth")
            curr_db = Database(db_path)  # 指定数据库文件路径
            data = curr_db.get_data()
            self.show_depth_info(data)
            self.current_item_data = data
            curr_db.close()

            self.jie_gu_count = len(data)
            self.label_3.setProperty("text", video_path.split('/')[-1])

            self.label_16.setProperty("text", "当前播放帧号 0 总帧数 {}".format(self.cur_total_frames))

    def jiegu_widget_item_selected(self):
        selected_items = self.treeWidget_5.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            idx = item.text(0)  # 序号
            idx_frame = item.text(1)  # 帧号
            sep_frame = item.text(2)  # 帧间隔
            frame_depth = item.text(3)  # 帧对应的深度

            info = "当前接箍号{} 深度 {}M".format(idx, frame_depth)
            self.label_28.setProperty("text", info)

            total_frame = self.cur_total_frames
            info1 = "当前接箍编号 {} 接箍总数 {}".format(idx, len(self.current_item_data))
            self.label_31.setProperty("text", info1)

            data = self.current_item_data

            self.jie_gu_count = len(data)

            # 当点击接箍item时，更新位置列表对应的图片
            position = int(idx_frame) / total_frame
            self.display_frame(self.selected_video_path, position, self.picture_label)

    def jiegu_widget_item_double_click(self):
        selected_items = self.treeWidget_5.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            idx_frame = item.text(1)  # 帧号
            frame_depth = item.text(3)  # 帧对应的深度
            # 把帧号和深度赋值到接箍对深的文本框里面
            self.frameLineEdit.setText(str(idx_frame))
            self.deepLineEdit.setText(str(frame_depth))

    def playOrStop(self):
        if self.player.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.player.mediaPlayer.stop()
            self.timer.stop()
            self.pushButton_10.setText('播放')
            self.pushButton_11.setText('继续')
            self.player.mediaPlayer.setPlaybackRate(1)
            self.spinBox.setValue(1)
            self.label_16.setProperty("text", "当前播放帧号 0 总帧数 {}".format(self.cur_total_frames))
        else:
            self.pushButton_10.setText("停止")
            self.pushButton_11.setText('暂停')
            self.player.mediaPlayer.play()
            self.timer.start(40)

    def pauseOrContinue(self):
        if self.player.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.player.mediaPlayer.pause()
            self.timer.stop()
            self.pushButton_10.setText('播放')
            self.pushButton_11.setText("继续")
            # 暂停后展示预览图
            is_end, position = self.player.getCurrentProgress()
            if is_end:
                return
            # 将帧图像转换为QPixmap并显示在QLabel上
            self.display_frame(self.selected_video_path, position, self.picture_label)
            # 接箍对深 帧号填写
            cur_duration, current_frame = self.player.get_current_frame()
            self.frameLineEdit.setText(str(current_frame))
            #self.lineEdit_5.setText(cur_duration)
            # 识别图像上的时间并填写到lineEdit_5上
            start = time.time()
            cap = cv2.VideoCapture(self.selected_video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, position)  # 设置当前帧位置
            ret, frame = cap.read()  # 读取当前帧
            if ret and self.checkBox_4.isChecked():
                text_list = ocr_image(frame)
                print(text_list)
                print("识别时间:", time.time() - start)
                if len(text_list) > 1:
                    valid_time = text_list[1]
                else:
                    valid_time = "未识别"
                self.lineEdit_5.setText(valid_time)

            is_end, current_frame = self.player.getCurrentProgress()
            if is_end:
                self.timer.stop()
            self.label_16.setProperty("text", "当前播放帧号 {} 总帧数 {}".format(current_frame, self.cur_total_frames))

        else:
            self.pushButton_10.setText('停止')
            self.pushButton_11.setText("暂停")
            self.player.mediaPlayer.play()
            self.timer.start(40)

    def display_frame(self, video_path, position, label):
        cap = cv2.VideoCapture(video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, position)  # 设置当前帧位置
        ret, frame = cap.read()  # 读取当前帧

        print("CheckBox is checked:", self.checkBox_2.isChecked())
        # 如果启用图像增强
        if self.checkBox_2.isChecked():
            mn = "cubic_x2"
            frame = super_resolution_with_modelname(frame, mn)

        # 改变亮度和对比度
        frame = adjust_brightness_contrast(frame, self.horizontalSlider.value(), self.horizontalSlider_2.value())

        default_config = load_config()
        x = int(default_config['x'])
        y = int(default_config['y'])
        font_size = float(default_config['font_size'])
        background_color = color_to_hex(default_config['background_color'])
        font_color = color_to_hex(default_config['font_color'])

        data = self.current_item_data

        if len(data) > 1:
            # 计算平均深度
            first_frame, first_depth, _ = data[0]
            last_frame, last_depth, _ = data[-1]
            # 计算插值
            avg_deep = (last_depth - first_depth) / (last_frame - first_frame)
            f0_deepth = first_depth - avg_deep * first_depth
            # 计算current_depth
            current_depth = position * avg_deep + f0_deepth
            # 在视频帧上添加深度信息水印
            depth_text = f"{current_depth:.3f} m"
            # 添加一个透明的黄色背景在depth_text下面
            depth_text_size = cv2.getTextSize(depth_text, cv2.FONT_HERSHEY_SIMPLEX, float(font_size), 2)[0]
            # 计算矩形的大小和位置
            rect_top_left = (x, y - 10)
            rect_bottom_right = (x + depth_text_size[0], y + depth_text_size[1] + 10)
            # 绘制填充矩形
            cv2.rectangle(frame, rect_top_left, rect_bottom_right, background_color, -1)
            # 绘制文本
            cv2.putText(frame, depth_text, (x, depth_text_size[1] + y), cv2.FONT_HERSHEY_SIMPLEX, float(font_size), font_color, 2,
                        cv2.LINE_AA)

        if ret:
            # 将OpenCV图像格式转换为Qt图像格式
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)

            # 将Qt图像显示在QLabel上
            label.setPixmap(QtGui.QPixmap.fromImage(qt_image))
        else:
            label.setText('Error: Failed to read frame')

        cap.release()

    def backSlider(self):
        # if self.player.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
        j_miao = int(1000/25 * int(self.spinBox_2.text()))
        self.player.mediaPlayer.setPosition(self.player.mediaPlayer.position() - j_miao)  # 1000/25秒，每次走一帧
        # 接箍对深 帧号填写
        _, position = self.player.getCurrentProgress()
        # 将帧图像转换为QPixmap并显示在QLabel上
        self.display_frame(self.selected_video_path, position, self.picture_label)
        cur_duration, current_frame = self.player.get_current_frame()
        self.label_16.setProperty("text", "当前播放帧号 {} 总帧数 {}".format(current_frame, self.cur_total_frames))
        self.frameLineEdit.setText(str(current_frame))
        #self.lineEdit_5.setText(cur_duration)

    def forwardSlider(self):
        # if self.player.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
        j_miao = int(1000/25 * int(self.spinBox_2.text()))
        self.player.mediaPlayer.setPosition(self.player.mediaPlayer.position() + j_miao)
        # 接箍对深 帧号填写
        _, position = self.player.getCurrentProgress()
        # 将帧图像转换为QPixmap并显示在QLabel上
        self.display_frame(self.selected_video_path, position, self.picture_label)
        cur_duration, current_frame = self.player.get_current_frame()
        self.label_16.setProperty("text", "当前播放帧号 {} 总帧数 {}".format(current_frame, self.cur_total_frames))
        self.frameLineEdit.setText(str(current_frame))
        #self.lineEdit_5.setText(cur_duration)

    def reversePlayback(self):
        show_warning_message_box("开发中，暂不支持")
        return
        state = self.player.mediaPlayer.state()
        if state == QtMultimedia.QMediaPlayer.StoppedState:
            self.player.setPosition(0)
            self.player.play()
        elif state == QtMultimedia.QMediaPlayer.EndOfMedia:
            self.player.setPosition(0)
            self.player.play()
        elif state == QtMultimedia.QMediaPlayer.PlayingState:
            self.player.mediaPlayer.setPlaybackRate(-1)  # 设置播放速度为负数

    def takeScreenshot(self):
        # 对self.player的当前帧进行截图并保存,保存的目录由用户决定
        # 弹出文件保存对话框，让用户选择保存目录和文件名
        options = QtWidgets.QFileDialog.Options()
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self.player, "保存", "", "PNG Files (*.png);;JPEG Files (*.jpeg)",
                                                  options=options)
        if not fileName:
            return

        _, position = self.player.getCurrentProgress()

        cap = cv2.VideoCapture(self.selected_video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, position)  # 设置当前帧位置
        ret, frame = cap.read()  # 读取当前帧

        is_spuerX = self.checkBox_2.isChecked()
        if is_spuerX:
            mn = "cubic_x2"
            frame = super_resolution_with_modelname(frame, mn)

        # 改变亮度和对比度
        frame = adjust_brightness_contrast(frame, self.horizontalSlider.value(), self.horizontalSlider_2.value())

        default_config = load_config()
        x = int(default_config['x'])
        y = int(default_config['y'])
        font_size = float(default_config['font_size'])
        background_color = color_to_hex(default_config['background_color'])
        font_color = color_to_hex(default_config['font_color'])

        data = self.current_item_data

        # 计算平均深度
        try:
            first_frame, first_depth, _ = data[0]
            last_frame, last_depth, _ = data[-1]
        except:
            first_frame, first_depth = data[0]
            last_frame, last_depth = data[-1]
        # 计算插值
        avg_deep = (last_depth - first_depth) / (last_frame - first_frame)
        f0_deepth = first_depth - avg_deep * first_depth
        # 计算current_depth
        current_depth = position * avg_deep + f0_deepth
        # 在视频帧上添加深度信息水印
        depth_text = f"{current_depth:.3f} m"
        # 添加一个透明的黄色背景在depth_text下面
        depth_text_size = cv2.getTextSize(depth_text, cv2.FONT_HERSHEY_SIMPLEX, font_size, 2)[0]
        # 计算矩形的大小和位置
        rect_top_left = (x, y - 10)
        rect_bottom_right = (x + depth_text_size[0], y + depth_text_size[1] + 10)
        # 绘制填充矩形
        cv2.rectangle(frame, rect_top_left, rect_bottom_right, background_color, -1)
        # 绘制文本
        cv2.putText(frame, depth_text, (x, depth_text_size[1] + y), cv2.FONT_HERSHEY_SIMPLEX, font_size, font_color, 2, cv2.LINE_AA)

        # 将帧保存为图片
        cv2.imwrite(fileName, frame)
        cap.release()

        print(f"截图已保存为{fileName}")

    # quit
    def handleQuit(self):
        self.player.handleQuit()

    def update_informations(self):
        is_end, current_frame = self.player.getCurrentProgress()
        if is_end:
            self.timer.stop()
        self.label_16.setProperty("text", "当前播放帧号 {} 总帧数 {}".format(current_frame, self.cur_total_frames))

    def add_depth_to_frame(self):
        # 根据对应的视频, 对应的帧添加深度信息, 并保存为txt文件
        selected_items = self.video_tree_widget.selectedItems()
        if not selected_items:
            show_warning_message_box("未选中视频")
            return

        flag_frame = self.frameLineEdit.text()
        flag_deepth = self.deepLineEdit.text()
        flag_time = self.lineEdit_5.text()

        if flag_frame == "" or flag_deepth == "" or flag_time == "":
            show_warning_message_box("信息填写不完整")
            return

        # 检测时间格式是否正确
        if not is_valid_time_format(flag_time):
            show_warning_message_box("时间格式不正确")
            return

        # 从deepth文件夹中对应的文本文件读取序号和深度信息, 如果读取不到设置序号为0
        db_path = "deepth/" + self.current_video + ".db"
        curr_db = Database(db_path)  # 指定数据库文件路径
        curr_db.add_data(int(flag_frame), float(flag_deepth), str(flag_time))
        data = curr_db.get_data()
        self.current_item_data = data
        self.show_depth_info(data)
        curr_db.close()

    def show_depth_info(self, data):
        # 清空self.treeWidget_5列表
        while self.treeWidget_5.topLevelItemCount() > 0:
            self.treeWidget_5.takeTopLevelItem(0)
        if len(data) > 0:
            self.treeWidget_5.addTopLevelItem(
                QtWidgets.QTreeWidgetItem(["1", str(data[0][0]), "0", str(data[0][1]), data[0][2], "00:00:00", " "]))

        for i in range(1, len(data)):
            current_frame = data[i][0]
            prev_frame = data[i - 1][0]
            current_time = data[i][2]
            prev_time = data[i - 1][2]
            frame_diff = current_frame - prev_frame
            time_diff = calculate_time_difference(current_time, prev_time)
            current_depth = data[i][1]
            # 将帧号和深度信息添加到接箍位置列表中
            self.treeWidget_5.addTopLevelItem(
                QtWidgets.QTreeWidgetItem([str(i + 1), str(current_frame), str(frame_diff), str(current_depth), current_time, time_diff, " "]))

    def select_folder(self):
        # 选择一个文件夹作为视频保存路径
        options = QtWidgets.QFileDialog.Options()
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self.player, "选择文件夹", "", options=options)
        if folder_path:
            self.save_path = folder_path
            self.lineEdit_4.setText(f"{self.save_path}")

    def start_handle_video(self):
        if self.checkBox_3.isChecked():
            print("开始处理所有视频")
            # 清空之前的操作
            self.video_operations.clear()
            # 添加选择操作到队列
            for item_index in range(self.video_tree_widget.topLevelItemCount()):
                item = self.video_tree_widget.topLevelItem(item_index)
                self.video_operations.append(item)
            # 执行队列中的操作
            self.process_next_video_operation()
        else:
            # 根据tab_widget当前选中的是picture_tab还是video_tab决定打开视频文件还是图片文件
            selected_items = self.video_tree_widget.selectedItems()
            if len(selected_items) > 0:
                self.handle_video()

    def process_next_video_operation(self):
        print("process_next_video_operation...", self.video_operations)
        if len(self.video_operations) > 0:
            item = self.video_operations.popleft()
            item.setSelected(True)
            self.video_widget_item_selected()
            self.handle_video()

    def pause_handle_video(self):
        if self.pushButton_9.text() == "暂停":
            self.video_handler.pause()
            self.video_handler_thread.wait()
            self.pushButton_9.setText("继续")
            print("pause handle video... ")
        else:
            self.video_handler.resume()
            self.video_handler_thread.start()
            self.pushButton_9.setText("暂停")
            print("start handle video... ")

    def handle_video(self):
        is_superX = self.checkBox.isChecked()  # 是否开启图像增强
        if self.pushButton_8.text() == "开始":
            # 停止上一个线程
            if self.video_handler is not None:
                self.video_handler.stop()
                self.video_handler_thread.quit()
                self.video_handler_thread.wait()
                self.video_handler = None
                self.video_handler_thread = None
                del self.video_handler_thread

            data = self.current_item_data

            if len(data) < 2:
                show_warning_message_box("请先添加深度信息!")
                return
            else:
                if self.checkBox_3.isChecked():
                    self.pushButton_8.setText("开始")
                else:
                    self.pushButton_8.setText("停止")
                # 计算平均深度
                try:
                    first_frame, first_depth, _ = data[0]
                    last_frame, last_depth, _ = data[-1]
                except:
                    first_frame, first_depth = data[0]
                    last_frame, last_depth = data[-1]
                # 计算插值
                avg_deep = (last_depth - first_depth) / (last_frame - first_frame)
                f0_deepth = first_depth - avg_deep * first_depth
                f_end_deepth = last_depth + avg_deep * (self.cur_total_frames - last_frame)
                # TODO: 修改0的深度信息
                data.insert(0, (1, f0_deepth))
                data.append((self.cur_total_frames, f_end_deepth))

            list_depth = []
            list_frame = []
            for i in range(1, len(data)):
                start_frame = data[i - 1][0]
                end_frame = data[i][0]
                start_depth = data[i - 1][1]
                end_depth = data[i][1]
                list_depth.append((start_depth, end_depth))
                list_frame.append((start_frame, end_frame))

            self.video_handler = VideoHandler(self.selected_video_path,
                                              self.save_path + "/" + self.current_video + ".mp4",
                                              list_depth, list_frame, 0, is_superX)
            self.video_handler_thread = QtCore.QThread()
            self.video_handler.moveToThread(self.video_handler_thread)
            # 连接信号与槽
            self.video_handler.progress_changed.connect(self.update_progress_bar)
            self.video_handler.processing_finished.connect(self.process_next_video_operation)
            self.video_handler_thread.started.connect(self.video_handler.run)
            self.video_handler_thread.start()
        else:
            self.pushButton_8.setText("开始")
            if self.video_handler is not None:
                self.video_handler.stop()
                self.video_handler_thread.quit()
                self.video_handler_thread.wait()
                self.video_handler = None
                self.video_handler_thread = None
                del self.video_handler_thread

    def handle_picture(self, pic_path):
        frame = cv2.imread(pic_path)
        current_depth = float(self.deepLineEdit.text())
        # 在图片上添加深度信息水印
        depth_text = f"{current_depth:.3f} m"

        # 添加一个透明的黄色背景在depth_text下面
        depth_text_size = cv2.getTextSize(depth_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        background_color = (79, 240, 255)  # 背景 255 250 227
        text_color = (0, 0, 0)  # 文本

        # 计算矩形的大小和位置
        rect_top_left = (15, depth_text_size[1] - 10)
        rect_bottom_right = (depth_text_size[0] + 30, depth_text_size[1] + 35)

        # 绘制填充矩形
        cv2.rectangle(frame, rect_top_left, rect_bottom_right, background_color, -1)

        # 绘制文本
        cv2.putText(frame, depth_text, (20, depth_text_size[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 1, text_color,
                    2, cv2.LINE_AA)
        pic_name = pic_path.split("/")[-1]
        # 将结果保存到“D:/users/picture/image.png”中
        cv2.imwrite(self.save_path + "/" + pic_name, frame)


    def update_progress_bar(self, process, frame):
        self.label_14.setProperty("text", self.selected_video_path.split('/')[-1] + "文件   处理进度: " + str(int(process)) + "%")
        self.progressBar.setValue(int(process))
        self.video_tree_widget.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        self.pushButton_9.setEnabled(False)
        if int(process) == 100:
            self.video_tree_widget.setEnabled(True)
            self.pushButton_8.setEnabled(True)
            self.pushButton_9.setEnabled(True)
            self.pushButton_8.setText("开始")
            self.pushButton_9.setText("暂停")

    def sort_picture_items(self):
        # 获取所有item，按照video_name进行排序
        items0 = [self.video_tree_widget.topLevelItem(i) for i in range(self.video_tree_widget.topLevelItemCount())]
        for item in items0:
            itx = item.text(1)
            if not "_" in itx:
                show_warning_message_box("视频文件名称格式不正确，无法排序")
                return
        sorted_items = sorted(items0,  key=lambda item: int(item.text(1).split("_")[1]))

        # 更新item顺序
        for i, item in enumerate(sorted_items):
            self.video_tree_widget.takeTopLevelItem(self.video_tree_widget.indexOfTopLevelItem(item))
            self.video_tree_widget.insertTopLevelItem(i, item)
            item.setText(0, str(i))

    def delete_seleted_row(self):
        if show_info_message_box():
            return
        # 删除选中行
        selected_items = self.treeWidget_5.selectedItems()
        selected_items1 = self.video_tree_widget.selectedItems()
        if not selected_items:
            return
        if not selected_items1:
            return

        for item in selected_items:
            idx_frame = item.text(1)  # 帧号
            # 删除数据库中的数据
            db_path = "deepth/" + self.current_video + ".db"
            curr_db = Database(db_path)  # 指定数据库文件路径
            curr_db.delete_data(int(idx_frame))
            data = curr_db.get_data()
            self.current_item_data = data
            self.show_depth_info(data)
            curr_db.close()

            parent = item.parent()
            if parent is None:
                # 顶级项目
                index = self.treeWidget_5.indexOfTopLevelItem(item)
                self.treeWidget_5.takeTopLevelItem(index)
            else:
                # 子级项目
                parent.takeChild(parent.indexOfChild(item))

    def export_to_excel(self):
        # 导出
        item = self.treeWidget_5.invisibleRootItem()
        if item is None:
            return

        # 选择文件夹
        options = QtWidgets.QFileDialog.Options()
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self.player, "选择文件夹", "", options=options)

        if not folder_path:
            return

        child_count = item.childCount()
        data = []
        for i in range(child_count):
            child_item = item.child(i)
            idx = child_item.text(0)  # 序号
            idx_frame = child_item.text(1)  # 帧号
            sep_frame = child_item.text(2)  # 帧间隔
            frame_depth = child_item.text(3)  # 帧对应的深度
            data.append((idx, idx_frame, sep_frame, frame_depth))

        # 创建DataFrame
        df = pd.DataFrame(data, columns=['序号', '帧号', '帧间隔', '深度'])

        full_path = os.path.join(folder_path, self.current_video + ".xlsx")
        # 将DataFrame保存为excel文件
        df.to_excel(full_path, index=False)

    # 设置-确定
    def update_video_watermark(self):
        x = 0
        y = 0
        fontsize = 1.3
        background_color = "#FFFFFF"
        font_color = "#000000"

        folder = os.path.dirname(watermark_save_path)
        if not os.path.exists(folder):
            os.makedirs(folder)

        # 将x, y, fontsize, background_color, font_color, 保存到txt文件中
        with open(watermark_save_path + "", "w") as f:
            f.write(str(x) + "\n")
            f.write(str(y) + "\n")
            f.write(str(fontsize) + "\n")
            f.write(str(background_color) + "\n")
            f.write(str(font_color) + "\n")

    # 设置-重置
    def resetting_video_watermark(self):
        if os.path.exists(watermark_save_path):
            os.remove(watermark_save_path)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    window = QtWidgets.QMainWindow()
    ui = Modifier()
    ui.setupUi(window)
    ui.modify_frame()
    window.show()
    sys.exit(app.exec_())

