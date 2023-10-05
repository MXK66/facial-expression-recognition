"""
功能：导入训练好的模型，遍历测试集进行预测，计算混淆矩阵并绘图输出，保存
运行plot_confusion_matrix.py需要
    keras 2.2.4
    pandas 0.24.2
    scikit-learn 0.21.2
    tensorflow 1.13.1
    opencv-python 4.10.25
    matplotlib 3.2.1
"""
import warnings
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings(action='ignore')
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
import cv2
from keras.models import load_model
from load_and_process import load_fer2013, preprocess_input
from sklearn.model_selection import train_test_split



# 表情分类标签
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]
# 模型位置
emotion_model_path = 'models/_mini_XCEPTION.102-0.66.hdf5'
emotion_model = load_model(emotion_model_path, compile=False)  # 载入模型
input_shape = emotion_model.input_shape[1:]  # 模型的输入大小

#

# 载入数据集
faces, emotions = load_fer2013()
faces = preprocess_input(faces)
num_samples, num_classes = emotions.shape

# 划分的训练、测试集
xtrain, xtest, ytrain, ytest = train_test_split(faces, emotions, test_size=0.2, shuffle=True)

# 利用训练好的模型对测试集进行预测
ndata = xtest.shape[0]  # 测试集数据量
y_pred = np.zeros((ndata,))  # 用于保存预测的结果
y_true = [ytest[i].argmax() for i in range(ndata)]  # 获取真实标签
y_true = np.array(y_true)  # 矩阵化

# 遍历测试集，获得预测结果
for i in range(ndata):
    input_image = xtest[i]
    input_image = cv2.resize(input_image, input_shape[0:2], cv2.INTER_NEAREST)
    # 确保输入尺寸与模型输入一致
    input_image = np.reshape(input_image, (1, input_shape[0], input_shape[1], input_shape[2]))
    # 调用模型对每张图片进行预测
    preds = emotion_model.predict(input_image)[0]
    y_pred[i] = preds.argmax()  # 最大值位置为最终结果

tick_marks = np.array(range(len(EMOTIONS))) + 0.5

import pandas as pd
import seaborn as sns
from sklearn.metrics import classification_report

# 生成分类报告
report = classification_report(y_true, y_pred, target_names=EMOTIONS, output_dict=True)

# 将分类报告转化为DataFrame格式
report_df = pd.DataFrame(report).transpose()

# 选取需要展示的指标列
report_df = report_df[['precision', 'recall', 'f1-score', 'support']]

# 将DataFrame中的数值格式化为百分数
report_df.iloc[:, :-1] = report_df.iloc[:, :-1].apply(lambda x: x.apply(lambda y: '{:.2%}'.format(y)))
# Add this line to remove percentage sign and convert string to float
report_df.iloc[:, :-1] = report_df.iloc[:, :-1].apply(lambda x: x.str.replace('%', '')).astype(float)

# 使用heatmap函数生成热力图
sns.heatmap(report_df, annot=True, cmap='Blues', fmt='', cbar=False)
plt.title('Classification Report')
plt.show()



def plot_confusion_matrix(cm, title='Confusion Matrix', cmap=plt.cm.binary):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    xlocations = np.array(range(len(EMOTIONS)))
    plt.xticks(xlocations, EMOTIONS, rotation=45)
    plt.yticks(xlocations, EMOTIONS)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


# 计算混淆矩阵
cm = confusion_matrix(y_true, y_pred)
np.set_printoptions(precision=2)  # 设置精度
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]  # 各类比率
print('混淆矩阵：')
print(cm_normalized)
accuracy = np.mean([cm_normalized[i, i] for i in range(num_classes)])  # 混淆矩阵右斜线上的结果之和的均值即为准确率
print('准确率：' + str(round(accuracy, 2)))

# 创建窗口，绘制混淆矩阵图
plt.figure(figsize=(12, 8), dpi=120)
ind_array = np.arange(len(EMOTIONS))
x, y = np.meshgrid(ind_array, ind_array)

# 添加每格分类比率结果
for x_val, y_val in zip(x.flatten(), y.flatten()):
    c = cm_normalized[y_val][x_val]
    if c > 0.01:
        plt.text(x_val, y_val, "%0.2f" % (c,), color='red', fontsize=10, va='center', ha='center')
# 设置图表
plt.gca().set_xticks(tick_marks, minor=True)
plt.gca().set_yticks(tick_marks, minor=True)
plt.gca().xaxis.set_ticks_position('none')
plt.gca().yaxis.set_ticks_position('none')
plt.grid(False, which='minor', linestyle='-')
plt.gcf().subplots_adjust(bottom=0.15)

# 显示绘图
plot_confusion_matrix(cm_normalized, title='Normalized confusion matrix')
plt.savefig('confusion_matrix.png', format='png')  # 保存结果
plt.show()  # 显示窗口




