import pandas as pd
import cv2
import numpy as np
# `load_fer2013`函数读取FER2013数据集中的数据。它首先使用pandas库读取CSV文件，并将像素列转换为列表。然后，它
# 遍历每个像素序列，将像素值拆分为列表，并将其重新调整为48x48的矩阵。最后，它将所有脸部图像存储在一个数组中，并将情绪标签进行独热编码。函数返回脸部图像数组和情绪标签数组。

dataset_path = 'fer2013/fer2013/fer2013.csv'
image_size=(48,48)
def load_fer2013():
    data = pd.read_csv(dataset_path)# 使用 Pandas 的 read_csv 函数从指定的数据集路径 dataset_path 中读取 CSV 文件，并将其存储在名为 data 的 DataFrame 中。
    pixels = data['pixels'].tolist()# 通过访问 data DataFrame 的 'pixels' 列，将像素数据提取为一个列表，并存储在名为 pixels 的变量中。
    faces = []# 创建一个空列表 faces，用于存储处理后的面部图像。
    for pixel_sequence in pixels:# 使用 for 循环遍历 pixels 列表中的每个像素序列。
        face = [int(pixel) for pixel in pixel_sequence.split(' ')]# 在每次迭代中，将像素序列拆分为单个像素值，并将其转换为整数类型。
        face = np.asarray(face).reshape(48, 48)# 将整数像素值转换为 NumPy 数组，并使用 reshape 函数将其重新塑造为一个 48x48 的面部图像。
        faces.append(face.astype('float32'))# 将处理后的面部图像添加到 faces 列表中，并转换为 'float32' 数据类型。
    faces = np.asarray(faces)# 将 faces 列表转换为 NumPy 数组，并使用 np.expand_dims 函数在最后一个维度上添加一个维度。这通常用于将图像数据扩展为适合模型输入的形状。
    faces = np.expand_dims(faces, -1)
    emotions = pd.get_dummies(data['emotion']).to_numpy()# 使用 Pandas 的 get_dummies 函数将情绪标签列进行独热编码，并将其转换为 NumPy 数组，并将结果存储在名为 emotions 的变量中。
    return faces, emotions
# `preprocess_input`函数对输入数据进行预处理。它将输入数据转换为`float32`类型，并将像素值缩放到0
                                   # 到1的范围内。如果参数`v2`为True，它还会将像素值进行归一化，使其在-1到1之间。函数返回预处理后的数据。



# x_normalized = (x - min) / (max - min)
# 调整为 -1 到 1：
# 当将像素值调整为 -1 到 1 时，像素值的范围从最小值到最大值映射到 -1 到 1 的范围。这样的调整
# 通常用于使数据分布在均值为 0 的范围内，有助于处理数据的中心化。这种调整可以帮助模型更容易地学习数据中的正负关系，特别是对于具有负面和正面影响的数据。
# 调整为 0 到 1：
# 当将像素值调整为 0 到 1 时，像素值的范围从最小值到最大值映射到 0 到 1 的范围。这种调整常用于将数据归一化到固定的范围，使得所有的像素
# 值都在相对相同的比例下进行比较和处理。这样的调整可以保留数据之间的相对关系，并且适用于许多机器学习算法，如神经网络模型。
def preprocess_input(x, v2=True):
    x = x.astype('float32')# 将输入数据 x 的数据类型转换为 'float32' 类型，使用 astype('float32') 方法。
    x = x / 255.0# 将输入数据 x 进行归一化，通过除以 255.0，使得像素值在 0 到 1 之间。
    if v2:# 如果 v2 参数为 True，执行以下操作：
        x = x - 0.5# 将归一化后的数据 x 减去 0.5，使得像素值的范围变为 -0.5 到 0.5。
        x = x * 2.0# 将数据 x 乘以 2.0，将像素值的范围调整为 -1 到 1。
    return x