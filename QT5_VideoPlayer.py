# -*- coding: utf-8 -*-

from PyQt5.QtGui import QKeySequence, QIcon, QPalette
from PyQt5.QtCore import QDir, Qt, QUrl, QPoint, QTime
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QVideoProbe
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLineEdit,
                            QPushButton, QSlider, QMessageBox, QStyle, QVBoxLayout,  
                            QWidget, QShortcut, QMenu)
import sys, cv2
import subprocess
#QT_DEBUG_PLUGINS

class VideoPlayer(QWidget):

    def __init__(self, aPath, parent=None):
        super(VideoPlayer, self).__init__(parent)

        self.setAttribute(Qt.WA_NoSystemBackground, True )
        self.setAcceptDrops(False)
        self.totalFrames = 1
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.StreamPlayback)
        self.mediaPlayer.mediaStatusChanged.connect(self.printMediaData)
        self.mediaPlayer.setVolume(80)
        self.videoWidget = QVideoWidget(self)

        self.lbl = QLineEdit('00:00:00')
        self.lbl.setReadOnly(True)
        self.lbl.setFixedWidth(70)
        self.lbl.setFixedHeight(40)
        self.lbl.setUpdatesEnabled(True)
        self.lbl.setStyleSheet(stylesheet(self))
        self.lbl.selectionChanged.connect(lambda: self.lbl.setSelection(0, 0))
        
        self.elbl = QLineEdit('00:00:00')
        self.elbl.setReadOnly(True)
        self.elbl.setFixedWidth(70)
        self.elbl.setFixedHeight(40)
        self.elbl.setUpdatesEnabled(True)
        self.elbl.setStyleSheet(stylesheet(self))
        self.elbl.selectionChanged.connect(lambda: self.elbl.setSelection(0, 0))

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setFixedWidth(32)
        self.playButton.setFixedHeight(40)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.setStyleSheet("background-color: black; border-radius: 0px;")
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal, self)
        self.positionSlider.setStyleSheet(stylesheet(self))
        self.positionSlider.setRange(0, 100)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.setSingleStep(1)
        self.positionSlider.setPageStep(20)
        self.positionSlider.setAttribute(Qt.WA_TranslucentBackground, True)
        self.positionSlider.setFixedHeight(40)

        self.myurl = ""
        
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.setSpacing(0)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.lbl)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(self.elbl)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.videoWidget)
        layout.addLayout(controlLayout)

        self.setLayout(layout)
        
        self.myinfo = "©2023 图宾智能\n\nMouse Wheel = Zoom\nUP = Volume Up\nDOWN = Volume Down\n" + \
                "LEFT = < 1 Minute\nRIGHT = > 1 Minute\n" + \
                "SHIFT+LEFT = < 10 Minutes\nSHIFT+RIGHT = > 10 Minutes"

        self.widescreen = True
        
        #### shortcuts ####
        self.shortcut = QShortcut(QKeySequence("q"), self)
        self.shortcut.activated.connect(self.handleQuit)
        # self.shortcut = QShortcut(QKeySequence("u"), self)

        # self.shortcut = QShortcut(QKeySequence("o"), self)
        self.shortcut.activated.connect(self.openFile)
        self.shortcut = QShortcut(QKeySequence(" "), self)
        self.shortcut.activated.connect(self.play)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Right), self)
        self.shortcut.activated.connect(self.forwardSlider)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Left), self)
        self.shortcut.activated.connect(self.backSlider)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Up), self)
        self.shortcut.activated.connect(self.volumeUp)
        self.shortcut = QShortcut(QKeySequence(Qt.Key_Down), self)
        self.shortcut.activated.connect(self.volumeDown)    
        self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier + Qt.Key_Right), self)
        self.shortcut.activated.connect(self.forwardSlider10)
        self.shortcut = QShortcut(QKeySequence(Qt.ShiftModifier + Qt.Key_Left), self)
        self.shortcut.activated.connect(self.backSlider10)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        # 创建QVideoProbe
        self.videoProbe = QVideoProbe()
        self.videoProbe.setSource(self.mediaPlayer)
        # # 连接videoFrameProbed信号的槽函数
        # self.videoProbe.videoFrameProbed.connect(self.handleFrame)

        print("Player started")
        print("press 'o' to open file (see context menu for more)")
        self.suspend_screensaver()


    def suspend_screensaver(self):
        'suspend linux screensaver'
        proc = subprocess.Popen('gsettings set org.gnome.desktop.screensaver idle-activation-enabled false', shell=True)
        proc.wait()

    def resume_screensaver(self):
        'resume linux screensaver'
        proc = subprocess.Popen('gsettings set org.gnome.desktop.screensaver idle-activation-enabled true', shell=True)
        proc.wait()

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie",
                QDir.homePath() + "/Videos", "Media (*.webm *.mp4 *.ts *.avi *.mpeg *.mpg *.mkv *.VOB *.m4v *.3gp *.mp3 *.m4a *.wav *.ogg *.flac *.m3u *.m3u8)")

        if fileName != '':
            self.loadFilm(fileName)
            print("File loaded")

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    
    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.mediaPlayer.position())
        self.lbl.setText(mtime.toString())

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(self.mediaPlayer.duration())
        self.elbl.setText(mtime.toString())

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        print("Error: ", self.mediaPlayer.error)

    def handleQuit(self):
        self.mediaPlayer.stop()
        self.resume_screensaver()
        print("Goodbye ...")

    def wheelEvent(self,event):
        mwidth = self.frameGeometry().width()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mscale = event.angleDelta().y() / 5
        if self.widescreen == True:
            self.setGeometry(mleft, mtop, mwidth + mscale, round((mwidth + mscale) / 1.778))
        else:
            self.setGeometry(mleft, mtop, mwidth + mscale, round((mwidth + mscale) / 1.33))


    def screen169(self):
        self.widescreen = True
        mwidth = self.frameGeometry().width()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mratio = 1.778
        self.setGeometry(mleft, mtop, mwidth, round(mwidth / mratio))

    def screen43(self):
        self.widescreen = False
        mwidth = self.frameGeometry().width()
        mleft = self.frameGeometry().left()
        mtop = self.frameGeometry().top()
        mratio = 1.33
        self.setGeometry(mleft, mtop, mwidth, round(mwidth / mratio))
    
    def forwardSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() + 1000*60)

    def forwardSlider10(self):
            self.mediaPlayer.setPosition(self.mediaPlayer.position() + 10000*60)

    def backSlider(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 1000*60)

    def backSlider10(self):
        self.mediaPlayer.setPosition(self.mediaPlayer.position() - 10000*60)
        
    def volumeUp(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() + 10)
        print("Volume: " + str(self.mediaPlayer.volume()))
    
    def volumeDown(self):
        self.mediaPlayer.setVolume(self.mediaPlayer.volume() - 10)
        print("Volume: " + str(self.mediaPlayer.volume()))
    
    # def mousePressEvent(self, evt):
    #     self.oldPos = evt.globalPos()

    # def mouseMoveEvent(self, evt):
    #     delta = QPoint(evt.globalPos() - self.oldPos)
    #     self.move(self.x() + delta.x(), self.y() + delta.y())
    #     self.oldPos = evt.globalPos()
            
        
    # def dragEnterEvent(self, event):
    #     if event.mimeData().hasUrls():
    #         event.accept()
    #     elif event.mimeData().hasText():
    #         event.accept()
    #     else:
    #         event.ignore()
    
    def loadFilm(self, f):
        # 获取总帧率
        self.totalFrames = cv2.VideoCapture(f).get(cv2.CAP_PROP_FRAME_COUNT)
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(f)))
        self.playButton.setEnabled(True)
        self.mediaPlayer.play()

    # def handleFrame(self, frame):
    #     # 获取当前帧数并更新UI
    #     currentFrameNumber = frame.currentFrameNumber()
    #     print("Current Frame Number:", currentFrameNumber)

    def printMediaData(self):
        if self.mediaPlayer.mediaStatus() == 6:
            if self.mediaPlayer.isMetaDataAvailable():
                res = str(self.mediaPlayer.metaData("Resolution")).partition("PyQt5.QtCore.QSize(")[2].replace(", ", "x").replace(")", "")
                print("%s%s" % ("Video Resolution = ",res))
                if int(res.partition("x")[0]) / int(res.partition("x")[2]) < 1.5:
                    self.screen43()
                else:
                    self.screen169()
            else:
                print("no metaData available")
      
    def openFileAtStart(self, filelist):
            matching = [s for s in filelist if ".myformat" in s]
            if len(matching) > 0:
                self.loadFilm(matching)

    def getCurrentProgress(self):
        # 获取当前播放时间和总时长
        position = self.mediaPlayer.position()
        duration = self.mediaPlayer.duration()
        try:
            # 当前视频帧,取整数
            currentFrame = int(self.totalFrames * position / duration)
        except:
            currentFrame = 0
        return currentFrame == self.totalFrames, currentFrame

    def get_current_frame(self):
        # 获取当前播放时间和总时长
        position = self.mediaPlayer.position()
        duration = self.mediaPlayer.duration()
        mtime = QTime(0, 0, 0, 0)
        mtime = mtime.addMSecs(position)
        time_str = mtime.toString()
        try:
            # 当前视频帧,取整数
            currentFrame = int(self.totalFrames * position / duration)
        except:
            currentFrame = 0
        return time_str, currentFrame



##################### end ##################################

def stylesheet(self):
    return """

QSlider::handle:horizontal 
{
background: transparent;
width: 8px;
}

QSlider::groove:horizontal {
border: 1px solid #444444;
height: 8px;
     background: qlineargradient(y1: 0, y2: 1,
                                 stop: 0 #2e3436, stop: 1.0 #000000);
}

QSlider::sub-page:horizontal {
background: qlineargradient( y1: 0, y2: 1,
    stop: 0 #729fcf, stop: 1 #2a82da);
border: 1px solid #777;
height: 8px;
}

QSlider::handle:horizontal:hover {
background: #2a82da;
height: 8px;
width: 18px;
border: 1px solid #2e3436;
}

QSlider::sub-page:horizontal:disabled {
background: #bbbbbb;
border-color: #999999;
}

QSlider::add-page:horizontal:disabled {
background: #2a82da;
border-color: #999999;
}

QSlider::handle:horizontal:disabled {
background: #2a82da;
}

QLineEdit
{
background: black;
color: #ffffff;
border: 0px solid #076100;
font-size: 8pt;
font-weight: bold;
}
    """

if __name__ == '__main__':

    app = QApplication(sys.argv)
    player = VideoPlayer('')
    player.setAcceptDrops(True)
    player.setWindowTitle("Video Player")
    player.setWindowIcon(QIcon.fromTheme("multimedia-video-player"))
    player.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    player.setGeometry(0, 0, 600, 380)
    player.setContextMenuPolicy(Qt.CustomContextMenu);
    player.show()
    player.widescreen = True
    if len(sys.argv) > 1:
        print(sys.argv[1])
        player.loadFilm(sys.argv[1])
    sys.exit(app.exec_())
