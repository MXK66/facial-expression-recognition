# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMovie
from real_time_video_me import Emotion_Rec
from os import getcwd
import numpy as np
import cv2
import time
from base64 import b64decode
from os import remove
from slice_png import img as bgImg
from EmotionRecongnition_UI import Ui_MainWindow
import image1_rc

class Emotion_MainWindow(Ui_MainWindow):
    def __init__(self, MainWindow):
        self.path = getcwd()#获取当前工作目录，并将其赋值给self.path。


        self.timer_camera = QtCore.QTimer()  # 定时器
        self.timer_video = QtCore.QTimer()  # 定时器用于定时触发相关操作。

        self.setupUi(MainWindow)
        self.retranslateUi(MainWindow)#设置主窗口的用户界面和翻译界面的文本。
        self.slot_init()  # 槽函数设置

        # # 设置界面动画
        # gif = QMovie(':/newPrefix/icons/scan.gif')
        # self.label_face.setMovie(gif)
        # gif.start()

        self.cap = cv2.VideoCapture()  # 屏幕画面对象
        self.cap2 = cv2.VideoCapture()#用于捕获屏幕画面和视频流。
        self.CAM_NUM = 0  # 摄像头标号将摄像头标号设置为0，表示默认使用第一个摄像头。
        self.model_path = None  # 模型路径将模型路径设置为None，表示未指定模型路径。
        # self.__flag_work = 0
    def slot_init(self):  # 定义槽函数
        self.toolButton_camera.clicked.connect(self.button_open_camera_click)
        self.toolButton_model.clicked.connect(self.choose_model)
        self.toolButton_video.clicked.connect(self.button_open_video_click)

        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_video.timeout.connect(self.show_video)
        self.toolButton_file.clicked.connect(self.choose_pic)
        # 在这个程序中，定时器的超时事件被用于实现实时视频处理和显示。具体来说，有两个定时器被使用：
        # `self.timer_camera`：该定时器用于捕获摄像头画面并进行情绪识别。它的超时事件绑定到 `self.show_camera`
        # 方法上，即每当定时器超时时，就会调用`self.show_camera`方法。这样可以定期获取摄像头画面，并对画面进行情绪识别，并将结果显示在界面上。
        # `self.timer_video`：该定时器用于处理和显示选择的视频文件。它的超时事件绑定到 `self.show_video`方法上，即每当定时器超时时，就会调用`self.show_video`
        # 方法。这样可以定期获取视频文件的帧，进行情绪识别，并将结果显示在界面上。
        # 通过定时器的超时事件，程序能够以固定的时间间隔进行画面获取和处理，从而实现实时的情绪识别和结果展示。
    def button_open_camera_click(self):
        # 在打开相机之前，对界面进行处理的目的是确保相机和界面处于正确的初始状态。这样做有以下几个原因：
        # 1. ** 停止定时器 **：如果之前有定时器在运行，首先需要停止定时器，以免与打开相机后的定时器冲突。这样可以确保相机捕获图像的频率和界面刷新的频率保持一致。
        # 2. ** 释放相机资源 **：在打开相机之前，需要释放之前打开的相机资源。这样可以确保在打开新的相机之前，之前的相机已经被关闭，避免资源的冲突和浪费。
        # 3. ** 清除标签内容 **：在打开相机之前，需要清除之前显示的标签内容。这样可以确保界面上的标签显示为空白状态，为后续显示新的图像或结果做好准备。
        # 通过对界面进行处理，可以确保相机和界面处于正确的状态，避免潜在的问题和冲突，并为后续的相机打开操作做好准备。
        # 界面处理
        self.timer_camera.stop()
        self.timer_video.stop()
        self.cap.release()
        self.cap2.release()
        self.label_face.clear()
        self.label_result.setText('None')
        self.label_time.setText('0 s')
        self.textEdit_camera.setText('实时摄像已关闭')
        self.textEdit_video.setText("视频未选中")
        self.label_outputResult.clear()

        # self.label_outputResult.setStyleSheet("border-image: url(:/newPrefix/icons/ini.png);")

        if self.timer_camera.isActive() == False:  # 检查定时状态
            flag = self.cap.open(self.CAM_NUM)  # 检查相机状态
            # 在if语句块中，首先尝试打开摄像头，使用self.cap.open(self.CAM_NUM)
            # 方法，其中self.CAM_NUM表示摄像头的编号。如果打开成功，则进行一系列界面处理，如清除之前的显示内容、设置文本信息等。然后，新建一个Emotion
            # _Rec对象，用于进行情绪识别。最后，启动定时器self.timer_camera.start(30)，以指定的时间间隔（30
            # 毫秒）触发相应的槽函数，实现实时显示摄像头画面和进行情绪识别。

            if flag == False:  # 相机打开失败提示
                msg = QtWidgets.QMessageBox.warning(self.centralwidget, u"Warning",
                                                    u"请检测相机与电脑是否连接正确！ ",
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)

            else:
                # 准备运行识别程序
                self.textEdit_pic.setText('文件未选中')
                QtWidgets.QApplication.processEvents()
                self.textEdit_camera.setText('实时摄像已开启')
                self.label_face.setText('正在启动识别系统...\n\nleading') # 定义文本内容
                # 新建对象
                self.emotion_model = Emotion_Rec(self.model_path)
                QtWidgets.QApplication.processEvents()
                # 打开定时器
                self.timer_camera.start(30)
        else:
            # 定时器未开启，界面回复初始状态
            # 如果定时器已经处于活动状态（即摄像头已经打开），则执行else语句块。在else语句块中，将定时器停止、释放摄像头资源，并进行一系列界面处理，使界面回到初始状态，包括清除显示内容、设置文本信息等。
            self.timer_camera.stop()
            self.timer_video.stop()
            self.cap.release()
            self.cap2.release()
            self.label_face.clear()
            self.textEdit_camera.setText('实时摄像已关闭')
            self.textEdit_pic.setText('文件未选中')
            self.textEdit_video.setText('文件未选中')
            # gif = QMovie(':/newPrefix/icons/scan.gif')
            # self.label_face.setMovie(gif)
            # gif.start()
            self.label_outputResult.clear()
            # self.label_outputResult.setStyleSheet("border-image: url(:/newPrefix/icons/ini.png);")

            self.label_result.setText('None')
            self.label_time.setText('0 s')
    def button_open_video_click(self):
        # 界面处理
        self.timer_camera.stop()
        self.timer_video.stop()
        self.cap.release()
        self.cap2.release()
        self.label_face.clear()
        self.label_result.setText('None')
        self.label_time.setText('0 s')
        self.textEdit_camera.setText('实时摄像已关闭')
        self.textEdit_video.setText("视频未选中")
        self.label_outputResult.clear()
        # self.label_outputResult.setStyleSheet("border-image: url(:/newPrefix/icons/ini.png);")

        if self.timer_video.isActive() == False:  # 检查定时状态
            # 使用文件选择对话框选择图片
            fileName_choose, filetype = QFileDialog.getOpenFileName(
                self.centralwidget, "选取图片文件",
                self.path,  # 起始路径
                "视频(*.mp4;)")  # 文件类型
            self.path = fileName_choose  # 保存路径
            if fileName_choose != '':
                self.textEdit_video.setText(fileName_choose + '文件已选中')
                # 新建对象
                self.cap2 = cv2.VideoCapture(self.path)
                self.emotion_model = Emotion_Rec(self.model_path)
                # 打开定时器
                self.label_face.setText('正在启动识别系统...\n\nleading')
                self.timer_video.start(30)
                QtWidgets.QApplication.processEvents()
            else:
                # 准备运行识别程序
                self.textEdit_pic.setText('文件未选中')
                self.textEdit_video.setText('文件未选中')
                QtWidgets.QApplication.processEvents()
                self.textEdit_camera.setText('实时摄像已关闭')

        else:
            # 定时器未开启，界面回复初始状态
            self.timer_camera.stop()
            self.timer_video.stop()
            self.cap.release()
            self.cap2.release()
            self.label_face.clear()
            self.textEdit_camera.setText('实时摄像已关闭')
            self.textEdit_pic.setText('文件未选中')
            self.textEdit_video.setText('文件未选中')
            # gif = QMovie(':/newPrefix/icons/scan.gif')
            # self.label_face.setMovie(gif)
            # gif.start()
            self.label_outputResult.clear()
            # self.label_outputResult.setStyleSheet("border-image: url(:/newPrefix/icons/ini.png);")

            self.label_result.setText('None')
            self.label_time.setText('0 s')

    def show_camera(self):
        # 定时器槽函数，每隔一段时间执行
        flag, self.image = self.cap.read()  # 获取画面
        self.image = cv2.flip(self.image, 1)  # 左右翻转

        # tmp = open('slice.png', 'wb')
        # tmp.write(b64decode(bgImg))
        # tmp.close()
        # canvas = cv2.imread('slice.png')  # 用于数据显示的背景图片
        # remove('slice.png')

        time_start = time.time()  # 计时
        # 使用模型预测
        # self.image为读取（摄像头或者视频）的一帧图像，
        # self.label_face就是一串文本数据，没啥大的意义，就是让界面好看或者让人知道正在干啥，  把文本传进去
        # self.label_outputResult没用到
        result = self.emotion_model.run(self.image, self.label_face, self.label_outputResult)
        # result = self.emotion_model.run(self.image, canvas, self.label_face, self.label_outputResult)
        time_end = time.time()
        # 在界面显示结果
        self.label_result.setText(result)
        self.label_time.setText(str(round((time_end - time_start), 3)) + ' s')
    def show_video(self):
        # 定时器槽函数，每隔一段时间执行
        flag, self.image = self.cap2.read()  # 获取画面
#从视频捕获设备（self.cap2）中读取一帧图像，并将结果存储在变量 self.image 中。flag 表示读取是否成功的标志。
        # self.image = cv2.flip(self.image, 1)  # 左右翻转

        # tmp = open('slice.png', 'wb')
        # tmp.write(b64decode(bgImg))
        # tmp.close()
        # canvas = cv2.imread('slice.png')  # 用于数据显示的背景图片
        # remove('slice.png')

        time_start = time.time()  # 计时
        # 使用模型预测

        result = 'None'
        if self.image is not None:
             result = self.emotion_model.run(self.image, self.label_face, self.label_outputResult)

        time_end = time.time()
        # 在界面显示结果
        self.label_result.setText(result)
        self.label_time.setText(str(round((time_end - time_start), 3)) + ' s')#对时间差进行四舍五入，保留三位小数。然后，通过将结果转换为字符串并添加 ' s' 后缀，将其设置为 self.label_time 标签的文本。
    def choose_pic(self):
        # 界面处理
        self.timer_camera.stop()
        self.timer_video.stop()
        self.cap.release()
        self.cap2.release()
        self.label_face.clear()
        self.label_result.setText('None')
        self.label_time.setText('0 s')
        self.textEdit_camera.setText('实时摄像已关闭')
        self.textEdit_video.setText('文件未选中')
        self.label_outputResult.clear()
        # self.label_outputResult.setStyleSheet("border-image: url(:/newPrefix/icons/ini.png);")

        # 使用文件选择对话框选择图片
        fileName_choose, filetype = QFileDialog.getOpenFileName(
            self.centralwidget, "选取图片文件",
            self.path,  # 起始路径
            "图片(*.jpg;*.jpeg;*.png)")  # 文件类型
        self.path = fileName_choose  # 保存路径
        if fileName_choose != '':
            self.textEdit_pic.setText(fileName_choose + '文件已选中')
            self.label_face.setText('正在启动识别系统...\n\nleading')
            QtWidgets.QApplication.processEvents()
            # 生成模型对象
            self.emotion_model = Emotion_Rec(self.model_path)
            # `QtWidgets.QApplication.processEvents()`
            # 是一个用于处理Qt应用程序事件循环的方法。在使用Qt构建的图形用户界面(GUI)
            # 应用程序中，事件循环是一个重要的概念。它负责接收和处理用户输入、系统事件以及应用程序内部的事件。在事件循环中，应用程序会不断地接收事件并将其分发到相应的处理函数中。
            # `processEvents()`
            # 方法是用于显式处理事件循环的一个调用点。它会处理当前队列中的所有待处理事件，包括用户输入、绘图更新等。通过调用`processEvents()`，你可以立即处理等待中的事件，而不必等待事件循环的正常处理。
            # 通常情况下，在进行长时间运算或处理耗时任务时，如果不调用`processEvents()`，GUI将会被阻塞，用户可能会感觉到应用程序无响应。通过在适当的时机调用
            # `processEvents()`，可以保持界面的响应性，使用户能够与应用程序进行交互。需要注意的是，过度频繁地调用`processEvents()`
            # 可能会导致性能下降，因为它会中断当前的代码执行流程来处理事件。因此，建议在适当的时机调用 `processEvents()`，以平衡响应性和性能的需求。
            image = self.cv_imread(fileName_choose)  # 读取选择的图片
            # 计时并开始模型预测
            QtWidgets.QApplication.processEvents()

            # 加载模型也需要耗时，所以初次加载模型耗时会比较长
            # for i in [0,1,2,3,4,5]:
            #     time_start = time.time()
            #     result = self.emotion_model.run(image, canvas, self.label_face, self.label_outputResult)
            #     time_end = time.time()
            #     print(round((time_end - time_start), 3))

            time_start = time.time()
            result = self.emotion_model.run(image, self.label_face, self.label_outputResult)
            # result = self.emotion_model.run(image,  self.label_face, self.label_outputResult)
            time_end = time.time()
            # 显示结果5.18
            self.label_result.setText(result)
            self.label_time.setText(str(round((time_end - time_start), 3)) + ' s')

        else:
            # 选择取消，恢复界面状态
            self.textEdit_pic.setText('文件未选中')
            # gif = QMovie(':/newPrefix/icons/scan.gif')
            # self.label_face.setMovie(gif)
            # gif.start()
            self.label_outputResult.clear()  # 清除画面
            # self.label_outputResult.setStyleSheet("border-image: url(:/newPrefix/icons/ini.png);")
            self.label_result.setText('None')
            self.label_time.setText('0 s')
    def cv_imread(self, filePath):
        # 读取图片
        cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
        ## imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化
        ## cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)
        return cv_img
    def choose_model(self):
        # 选择训练好的模型文件
        self.timer_camera.stop()
        self.timer_video.stop()
        self.cap.release()
        self.cap2.release()
        self.label_face.clear()
        self.label_result.setText('None')
        self.label_time.setText('0 s')
        self.textEdit_camera.setText('实时摄像已关闭')
        self.textEdit_video.setText('文件未选中')
        self.textEdit_pic.setText('文件未选中')
        self.label_outputResult.clear()
        # self.label_outputResult.setStyleSheet("border-image: url(:/newPrefix/icons/ini.png);")

        # 调用文件选择对话框
        fileName_choose, filetype = QFileDialog.getOpenFileName(self.centralwidget,
                                                                "选取图片文件", getcwd(),  # 起始路径
                                                                "Model File (*.hdf5)")  # 文件类型

        # 该方法首先停止计时器，释放视频捕获设备，清除标签和文本字段以重置状态。
        # 然后，使用QFileDialog.getOpenFileName打开一个文件对话框，以允许用户选择一个模型文件（ *.hdf5文件）。
        # 如果选择了一个文件（fileName_choose不为空），则将文件路径存储在self.model_path变量中，并在textEdit_model部件中显示该路径。
        # 如果没有选择文件，该方法会假设将使用默认模型，并相应地更新textEdit_model部件。

        # 显示提示信息
        if fileName_choose != '':
            self.model_path = fileName_choose
            self.textEdit_model.setText(fileName_choose + ' 已选中')
        else:
            self.textEdit_model.setText('使用默认模型')

            # 是一个文本编辑部件（QTextEdit），用于显示选择的模型文件路径或默认模型的信息。

        # 恢复界面
        # gif = QMovie(':/newPrefix/icons/scan.gif')
        # self.label_face.setMovie(gif)
        # gif.start()
