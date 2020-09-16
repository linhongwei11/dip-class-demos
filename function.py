import cv2 as cv
import numpy as np


# 读取单张图片
def readimg(image):
    print("-----------start to read Image-------------")
    # 判断图像是否为空
    if image is None:
        print("the Mat is empty,fail to read")
    else:
        print("not empty")
    print(image.shape)
    # 读取图像形状的基本信息
    height = image.shape[0]
    width = image.shape[1]
    channels = image.shape[2]
    print(f"图像行数为：{height}")
    print(f"图像列数为：{width}")
    print(f"图像通道数为：{channels}")
    print(f"图像尺寸为：{image.size}")
    print(f"图像行数为：{height}")
    # 读取单张图片
    srcmat = cv.imread("d:/timg.jpg")
    if image is None:
        print("the Mat is empty,fail to read")
    # 转化为灰度图
    grymat = cv.cvtColor(srcmat, cv.COLOR_BGR2GRAY)
    # 保存图片
    cv.imwrite("d:/9.jpg", grymat)
    # 显示图片
    cv.imshow("srcmat", srcmat)
    cv.imshow("graymat", grymat)
    cv.waitKey(0)


# 通过opencv读取视频
def readvideo():
    capture = cv.VideoCapture("d:/2.mp4")
    if not capture.isOpened():
        print("Unable to open video!")
        return -1
    # 输出视频相关信息
    width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
    height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
    frames = capture.get(cv.CAP_PROP_FRAME_COUNT)
    print(f"width:{width}")
    print(f"height:{height}")
    print(f"frames:{frames}")
    
    # 重新保存视频
    filename = "d:/test.mp4"
    fps = capture.get(cv.CAP_PROP_FPS)
    code = cv.VideoWriter_fourcc(*'mp4v')
    width = int(width / 2)
    height = int(height / 2)
    size = (width, height)
    out = cv.VideoWriter(filename, code, fps, size)
    # 从视频中读取照片
    ret, frame = capture.read()
    if ret:
        resizeframe = cv.resize(frame, size)
        out.write(resizeframe)
        # 转化为灰度图
        gryframe = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # 显示图片
        cv.imshow("frame", frame)
        cv.imshow("resizeframe", resizeframe)
        cv.imshow("gryframe", gryframe)
        cv.waitKey(30)
        return 0


# 创建图像
def creat_image():
    # 创建3*3的3通道的矩阵
    # 分别代表行数、列数、通道数以及数据类型
    m0 = np.ones([3, 3, 3], np.uint8)
    m0.fill(255)
    print(m0)
    # 创建图像(初始化图像)
    src = np.zeros([400, 400, 3], np.uint8)
    # 给图像的b通道赋值
    src[:, :, 0] = np.ones([400, 400]) * 255
    cv.imshow("src", src)


def traverse(image):
    height = image.shape[0]
    width = image.shape[1]
    channels = image.shape[2]
    for row in range(height):
        for col in range(width):
            average = image[row, col, 0] / 3 + image[row, col, 1] / 3 + image[row, col, 2] / 3
            for cha in range(channels):
                image[row, col, cha] = average
    cv.imshow("image", image)
