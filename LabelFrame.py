import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QLabel

class LabelFrame(QLabel):
    def __init__(self, parent=None):
        super(LabelFrame, self).__init__()
        self.main_window = parent
        self.setAlignment(Qt.AlignCenter)  # 居中显示
        self.setMinimumSize(640, 480)
        self.setScaledContents(False)

    def update_frame(self, frame):
        if self.height() > self.width():
            width = self.width()
            height = int(frame.shape[0] * (width / frame.shape[1]))
        else:
            height = self.height()
            width = int(frame.shape[1] * (height / frame.shape[0]))
        frame = cv2.resize(frame, (width, height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # bgr -> rgb
        h, w, c = frame.shape  # 获取图片形状
        image = QImage(frame, w, h, 3 * w, QImage.Format_RGB888)
        pix_map = QPixmap.fromImage(image)

        self.setPixmap(pix_map)