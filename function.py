import cv2 as cv
import numpy as np
import math


# 第二周练习1 rgb通道分离，并显示出来
def image_split(image):
    # split函数，将多通道图像分离
    b_image, g_image, r_image = cv.split(image)
    # 显示图片
    cv.imshow("b_image", b_image)
    cv.imshow("g_image", g_image)
    cv.imshow("r_image", r_image)
    cv.waitKey(0)


# 练习2 调用本机摄像头
def readvideo():
    capture = cv.VideoCapture(0)
    # 读取一帧图像
    ret, frame = capture.read()
    if ret:
        cv.imshow("frame", frame)
        cv.waitKey(30)
    else:
        print("读取图像失败")


# 第二周练习3，opencv的基本绘图功能
def drawing(image):
    pt1 = (10, 10)
    pt2 = (100, 100)
    # 在目标图像上画线段
    cv.line(image, pt1, pt2, (255, 0, 0))
    left = (20, 20)
    right = (100, 200)

    # 在目标图像上画矩形
    """
        rectangle（） 函数模型：
            rectangle(CV_IN_OUT Mat& img, Rect rec,
                              const Scalar& color, int thickness = 1,
                              int lineType = LINE_8, int shift = 0);
    
    
            参数介绍：
            . ICV_IN_OUT Mat& img: CV_IN_OUT Mat& img
            . Rect rec: Rect类成员（包含矩形的左上角坐标以及长宽）
            . const Scalar& color:输出颜色信息
            . int thickness: 表示线的粗细
            . int lineType :邻接关系，一般设置默认值
            . int shift: 偏移，一般设0
    """
    cv.rectangle(image,left,right,(255,255,0))
    cv.imshow("line_mat", image)


# 练习4 直方图计算(遍历灰度图，画出直方图)
def histogram(grymat):
    # 图像初始化
    image = np.zeros([600, 600, 3], np.uint8)
    his = [0] * 256
    total = grymat.shape[0] * grymat.shape[1]
    # 遍历所有像素
    for row in range(grymat.shape[0]):
        for col in range(grymat.shape[1]):
            his[grymat[row, col]] += 1
    for num in range(256):
        pt1 = (num, 600)
        # 由于归一化后比较小，为了更直观，放大了
        loacal = math.ceil(his[num] / total * 6000)
        pt2 = (num, 600 - loacal)
        # 画线
        cv.line(image, pt1, pt2, (255, 0, 0))
    cv.imshow("histogram", image)
    cv.waitKey(0)
