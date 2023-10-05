# -*- coding: utf-8 -*-
"""
运行本项目需要安装的库：
    keras 2.2.4
    PyQt5 5.11.3
    pandas 0.24.2
    scikit-learn 0.21.2
    tensorflow 1.13.1
    imutils 0.5.2
    opencv-python 4.10.25
    matplotlib 3.2.1  # 注意：此依赖包为第二版新增，请注意安装

点击运行主程序runMain.py
"""
# 使用warnings模块将警告信息的输出设置为忽略。
# 导入Emotion_MainWindow类，该类实现了情绪识别的主窗口界面。
# 导入QApplication和QMainWindow类，用于创建应用程序和主窗口对象。
# 在if __name__ == '__main__':条件下，创建一个QApplication对象app。
# 创建一个QMainWindow对象window。
# 创建一个Emotion_MainWindow对象ui，并将window作为参数传递。
# 显示主窗口window。
# 调用app.exec_()方法启动应用程序的事件循环。
# 最后，调用exit()函数退出程序。

import warnings
import os
# 忽略警告
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings(action='ignore')
from EmotionRecongnition import Emotion_MainWindow
from sys import argv, exit
from PyQt5.QtWidgets import QApplication,QMainWindow
# 这段代码的主要作用是创建一个情绪识别应用程序的图形界面，并运行该应用程序。
# 1. 首先，代码导入了必要的库和模块。
# 2. 接下来，创建了一个 QApplication 对象 `app`，用于管理应用程序的事件循环和 GUI。
# 3. 然后，创建了一个 QMainWindow 对象 `window`，作为应用程序的主窗口。
# 4. 创建了一个 Emotion_MainWindow 对象 `ui`，并将 `window` 作为参数传递给它，用于初始化应用程序的界面。
# 5. 显示主窗口。
# 6. 最后，调用 `app.exec_()` 进入应用程序的事件循环，直到应用程序退出。

#PyQt5惯例
# app = QApplication(sys.argv)
#
# # 创建主窗口
# window = QMainWindow()
# window.setWindowTitle("空白 PyQt 项目")
# window.resize(400, 300)
#
# # 显示主窗口
# window.show()
#
# # 运行应用程序
# sys.exit(app.exec_())
if __name__ == '__main__':
    app = QApplication(argv)

    window = QMainWindow()
    ui = Emotion_MainWindow(window)
    # ui = Emotion_MainWindow(window)

    window.show()
    exit(app.exec_())
