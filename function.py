import cv2 as cv
import numpy as np


# 第三周练习1 肤色提取实验
def skinrecognition():
    # 打开摄像头，读取照片
    capture = cv.VideoCapture(0)
    success, frame = capture.read()
    if success:
        # 设定上下限阈值
        lower = np.array([0, 43, 55])
        upper = np.array([20, 255, 255])
        # 将图像转化为hsv
        hsv_mat = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        # 利用inRange函数筛选
        result_mat = cv.inRange(hsv_mat, lower, upper)
        cv.imshow("result", result_mat)
        cv.waitKey(30)


# 第三周练习2 图像二值化
def binarization():
    # 读取图片
    src = cv.imread("d:/timg.jpg")
    # 转化为灰度图
    gry_mat = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
    # 普通图像二值化
    ret, bin_mat = cv.threshold(gry_mat, 100, 255, cv.THRESH_BINARY)
    # 大津法图像二值化
    ret2, otsu_mat = cv.threshold(gry_mat, 100, 255, cv.THRESH_OTSU)
    # 区域自适应图像二值化
    adap_mat = cv.adaptiveThreshold(gry_mat, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 15, 10)
    cv.imshow("bin_mat", bin_mat)
    cv.imshow("otsu_mat", otsu_mat)
    cv.imshow("adap_mat", adap_mat)
    cv.waitKey(0)


# 第三周练习3创建一个滑动条，可通过移动滑动条调节二值化阈值
img = []


# 回调函数
def callback(m):
    # 获取trackbar的位置
    value = cv.getTrackbarPos("value", "image")
    # 图像二值化
    ret, binary_mat = cv.threshold(img, value, 255, cv.THRESH_BINARY)
    cv.imshow("image", binary_mat)


# 添加滑动条
def trackbar():
    global img
    srcmat = cv.imread("d:/timg.jpg")
    # 转化为灰度图
    img = cv.cvtColor(srcmat, cv.COLOR_BGR2GRAY)
    cv.imshow("image", img)
    # 创建滑动条
    cv.createTrackbar("value", "image", 0, 255, callback)
    cv.waitKey(0)
