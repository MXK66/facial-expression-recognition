# -*- coding: utf-8 -*-


import base64

# 你提供的代码定义了一个名为`pic2py`的函数，该函数用于将图像文件转换为Python文件。
#
# 函数的输入参数是图像文件的名称（包括路径）。函数首先以二进制模式打开图像文件，并使用base64
# 模块对图像文件进行编码。然后，将编码后的字符串写入一个以图像文件名为基础，扩展名为.py的Python文件中。
#
# 在代码的主程序部分，定义了一个名为`pics`的列表，包含了要转换的图像文件的路径。然后使用`pic2py`函数对每个图像文件进行转换，生成对应的Python文件。最后输出"ok"表示转换完成。
#
# 请注意，生成的Python文件中会定义一个名为`img`的变量，它包含了图像文件的base64编码字符串。
# 这段代码定义了一个函数 `pic2py`，用于将图像文件转换为 Py 文件，并将图像数据存储为字符串的形式。以下是代码的解释：
# 1. 函数 `pic2py(picture_name)` 接受一个参数 `picture_name`，表示图像文件的名称。



# 5. 将 Base64 字符串 `b64str` 使用 `.decode()` 方法解码为 Unicode 字符串。
# 6. 构造写入 Py 文件的数据字符串 `write_data`，其中 `%s` 部分被替换为解码后的 Base64 字符串。


# 9. 关闭 Py 文件。

# 这段代码的目的是将图像文件转换为 Py 文件，并将图像数据以字符串形式存储在生成的 Py 文件中。这种转换通常用于将图像等二进制数据嵌入到源代码中，以便在需要时动态加载和使用图像数据。

def pic2py(picture_name):
    """
    将图像文件转换为py文件
    :param picture_name:
    :return:
    """
    open_pic = open("%s" % picture_name, 'rb')# 2. 打开图像文件，并使用二进制模式 `'rb'` 进行读取，将其赋值给变量 `open_pic`。
    b64str = base64.b64encode(open_pic.read())# 3. 使用 `base64.b64encode()` 函数对打开的图像文件进行编码，将二进制数据转换为 Base64 字符串表示。
    open_pic.close()# 4. 关闭打开的图像文件
    # 注意这边b64str一定要加上.decode()
    write_data = 'img = "%s"' % b64str.decode()# 6. 构造写入 Py 文件的数据字符串 `write_data`，其中 `%s` 部分被替换为解码后的 Base64 字符串。
    f = open('%s.py' % picture_name.replace('.', '_'), 'w+')# 7. 打开以图像文件名为基础的 Py 文件，以写入模式 `'w+'` 进行操作，并将其赋值给文件对象 `f`。
    f.write(write_data)# 8. 使用文件对象 `f` 的 `write()` 方法将数据字符串 `write_data` 写入 Py 文件。
    f.close()

# 如果脚本作为主程序运行，则定义一个图像文件列表 `pics`，其中包含要转换的图像文件路径。
# 使用 `for` 循环遍历图像文件列表 `pics` 中的每个图像文件路径，并调用 `pic2py()` 函数将每个图像文件转换为 Py 文件。
# 输出字符串 `"ok"`。
if __name__ == '__main__':
    pics = ["./icons/abcd.png"]
    for i in pics:
        pic2py(i)
    print("ok")