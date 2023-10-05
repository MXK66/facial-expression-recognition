
import cv2
import imutils
import numpy as np
from PyQt5 import QtGui, QtWidgets
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from load_and_process import preprocess_input
# import dlib

class Emotion_Rec:
    def __init__(self, model_path=None):
        # Python类的一个特殊方法，用于在创建类的实例时进行初始化操作。在这个代码段中，它是一个类的构造方法，用于初始化具有指定模型路径的对象。
        # 载入数据和图片的参数
        detection_model_path = 'haarcascade_files/haarcascade_frontalface_default.xml'

        if model_path == None:  # 若未指定路径，则使用默认模型
            emotion_model_path = 'models/_mini_XCEPTION.144-0.65.hdf5'
        else:
            emotion_model_path = model_path

        # 载入人脸检测模型
        self.face_detection = cv2.CascadeClassifier(detection_model_path)  # 级联分类器

        # 载入人脸表情识别模型
        self.emotion_classifier = load_model(emotion_model_path, compile=False)
        # 表情类别
        self.EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised",
                         "neutral"]

    # label_face的作用是在GUI界面上显示人脸区域的图像。具体显示的图片是经过人脸检测并标记了人脸框的原
    # 始图像。在run函数中，通过对原始图像进行处理，在检测到的人脸区域绘制矩形框，并将处理后的图像显示在label_face上。
    # 这样，用户就可以在GUI界面上看到带有人脸框的图像
    def run(self, frame_in, label_face, label_result):

        # frame_in 摄像画面或图像
        # label_face 用于人脸显示画面的label对象
        # label_result 用于显示结果的label对象
        # 调节画面大小
        frame = imutils.resize(frame_in, width=300)  # 缩放画面

        # frame = cv2.resize(frame, (300,300))  # 缩放画面
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 转为灰度图



        # 检测人脸
        faces = self.face_detection.detectMultiScale(gray, scaleFactor=1.1,
                                                     minNeighbors=5, minSize=(30, 30),
                                                     flags=cv2.CASCADE_SCALE_IMAGE)
        # 使用级联分类器对灰度图像进行人脸检测，返回检测到的人脸位置信息，存储在faces变量中。
        preds = []  # 用于存储表情识别的预测结果。
        label = None  # 预测的标签
        (fX, fY, fW, fH) = None, None, None, None  # 人脸位置
        frameClone = frame.copy()  # 复制原始画面，用于在其上进行绘制，保持原始画面不被修改。

        if len(faces) > 0:
            # 根据ROI大小将检测到的人脸排序
            faces = sorted(faces, reverse=False, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))  # 根据人脸区域的大小对检测到的人脸进行排序，按照面积从小到大排序。

            for i in range(len(faces)):  # 遍历每张检测到的人脸，默认识别全部人脸
                # 如果只希望识别和显示最大的那张人脸，可取消注释此处if...else的代码段
                # if i == 0:
                #     i = -1
                # else:
                #     break

                (fX, fY, fW, fH) = faces[i]

                # 从灰度图中提取感兴趣区域（ROI），将其大小转换为与模型输入相同的尺寸，并为通过CNN的分类器准备ROI
                roi = gray[fY:fY + fH, fX:fX + fW]#从灰度图中提取感兴趣区域（ROI），即当前人脸区域。
                roi = cv2.resize(roi, self.emotion_classifier.input_shape[1:3])#将感兴趣区域的大小调整为与模型输入相同的尺寸。
                roi = preprocess_input(roi)
                roi = img_to_array(roi)#将预处理后的ROI转换为数组形式。
                roi = np.expand_dims(roi, axis=0)#为通过CNN的分类器准备ROI，即在数组的第0维度上添加一个维度。

                # 用模型预测各分类的概率
                preds = self.emotion_classifier.predict(roi)[0]#使用表情识别模型对ROI进行预测，得到各个分类的概率。
                # emotion_probability = np.max(preds)  # 最大的概率
                label = self.EMOTIONS[preds.argmax()]  # 选取最大概率的表情类

                # 圈出人脸区域并显示识别结果
                cv2.putText(frameClone, label, (fX, fY - 10),
                            cv2.FONT_HERSHEY_TRIPLEX, 0.4, (0, 255, 0), 1)#在复制的画面上绘制识别结果的文本标签。
                cv2.rectangle(frameClone, (fX, fY), (fX + fW, fY + fH), (255, 255, 0), 1)#在复制的画面上绘制人脸区域的矩形框。

        # canvas = 255* np.ones((250, 300, 3), dtype="uint8")
        # canvas = cv2.imread('slice.png', flags=cv2.IMREAD_UNCHANGED)
#5.8晚
        for (i, (emotion, prob)) in enumerate(zip(self.EMOTIONS, preds)):
            # 用于显示各类别概率
            text = "{}: {:.2f}%".format(emotion, prob * 100)
# 20235.18
            # 绘制表情类和对应概率的条形图
            # w = int(prob * 300) + 7
            # cv2.rectangle(canvas, (7, (i * 35) + 5), (w, (i * 35) + 35), (224, 200, 130), -1)
            # cv2.putText(canvas, text, (10, (i * 35) + 23), cv2.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 1)

        # 调整画面大小与界面相适应
        frameClone = cv2.resize(frameClone, (420, 280))

        # 在Qt界面中显示人脸
        show = cv2.cvtColor(frameClone, cv2.COLOR_BGR2RGB)#将BGR格式的图像转换为RGB格式，以便在界面上正确显示颜色。
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)#根据转换后的图像数据创建Qt图像对象。
        label_face.setPixmap(QtGui.QPixmap.fromImage(showImage))#label_face 是用于显示人脸区域的标签对象。在代码的最后部分，通过以下代码将人脸区域显示在 label_face 标签对象上：  让文本显示
        # 将图像对象设置为显示人脸区域的标签对象的图像。
        QtWidgets.QApplication.processEvents()
        #QtWidgets.QApplication.processEvents()的作用是在图像显示之后立即处理任何待处理的界面事件，以确保图像能
        # 够及时显示在界面上，而不会导致应用程序无响应。这样可以保持界面的流畅性和及时性。
#5.8晚
        # 在显示结果的label中显示结果
        # show = cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB)
        # showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        # label_result.setPixmap(QtGui.QPixmap.fromImage(showImage))

        return (label)
