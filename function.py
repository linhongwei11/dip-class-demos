import cv2 as cv
import numpy as np
import math


# 第7周练习1：改进图片旋转
def spin_correct():
    # 读取图片并判断图片是否读取成功
    srcmat = cv.imread("d:/lena.jpg")
    if srcmat is None:
        print("fail to read")
        return
    # 初始化旋转角度以及缩放尺度
    angle = -10.0
    scale = 1
    # 设置旋转中心
    center = (int(srcmat.shape[1] * 0.5), int(srcmat.shape[0] * 0.5))
    # 获得变换矩阵
    rot = cv.getRotationMatrix2D(center, angle, scale)
    cos = np.abs(rot[0, 0])
    sin = np.abs(rot[0, 1])
    width = int((srcmat.shape[0] * sin) + (srcmat.shape[1] * cos))
    height = int((srcmat.shape[0] * cos) + (srcmat.shape[1] * sin))
    # 调整仿射矩阵参数
    rot[0, 2] += (width / 2) - (srcmat.shape[1] // 2)
    rot[1, 2] += (height / 2) - (srcmat.shape[0] // 2)
    # 利用仿射变换函数
    warpmat = cv.warpAffine(srcmat, rot, (width, height))
    # 显示图像
    cv.imshow("warpmat", warpmat)
    cv.waitKey(0)


# 第7周练习2-3：霍夫变换的使用
# 标准霍夫变换
def houghdemo():
    # 读取图像，并判断是否读取成功
    srcmat = cv.imread("d:/img.png")
    if srcmat is None:
        print("failed to read image")
        return
    # canny函数边缘检测
    dx = cv.Sobel(srcmat, cv.CV_16S, 1, 0)
    dy = cv.Sobel(srcmat, cv.CV_16S, 0, 2)
    # 边缘提取
    canny_mat = cv.Canny(dx, dy, 60, 180)
    """
    HoughLines（） 函数模型：
        HoughLines( InputArray image, OutputArray lines,
                                  double rho, double theta, int threshold,
                                  double srn = 0, double stn = 0,
                                  double min_theta = 0, double max_theta = CV_PI );
    
        参数介绍：
        . InputArray image：InputArray类型的image，输入8bit、单通道
        . OutputArray lines：InputArray类型的lines，经过调用HoughLines函数后储存了霍夫线变换检测到线条的输出矢量
        . double rho：double类型的rho，以像素为单位的距离精度
        . double theta: double类型的theta，以弧度为单位的角度精度
        . int threshold: int类型的threshold，累加平面的阈值参数，即识别某部分为图中的一条直线时它在累加平面中必须达到的值
        . double srn: double类型的srn，有默认值0
        . double stn: double类型的stn，有默认值0，对于多尺度霍夫变换，srn表示第四个参数进步尺寸的单位角度theta的除数距离
        . double min_theta: double类型的 min_theta，对于标准和多尺度Hough变换，检查线条的最小角度
        . double max_theta: double类型的 max_theta, 对于标准和多尺度Hough变换，检查线条的最大角度
    """
    lines = cv.HoughLines(canny_mat, 1, np.pi / 180, 55)
    
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * a))
        pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * a))
        cv.line(srcmat, pt1, pt2, (255, 0, 0), 1)
    cv.imshow("canny_mat", canny_mat)
    cv.imshow("srcmat", srcmat)
    cv.waitKey(0)


# 累计概率霍夫变换
def houghsp_demo():
    srcmat = cv.imread("d:/img.png")
    if srcmat is None:
        print(" failed to read ")
        return
    
    # 转化为灰度图
    grymat = cv.cvtColor(srcmat, cv.COLOR_BGR2GRAY)
    # 边缘检测
    canny_mat = cv.Canny(grymat, 60, 180, 3)
    # 累计概率霍夫变换
    """
    HoughLinesP（） 函数模型：
        HoughLinesP( InputArray image, OutputArray lines,
                                   double rho, double theta, int threshold,
                                   double minLineLength = 0, double maxLineGap = 0 );
    
        参数介绍：
        . InputArray image：InputArray类型的image，输入8bit、单通道
        . OutputArray lines：InputArray类型的lines，经过调用HoughLinesP函数后后存储了检测到的线条的输出矢量，每一条线由具有四个元素的矢量(x_1,y_1, x_2, y_2）  表示，其中，(x_1, y_1)和(x_2, y_2) 是是每个检测到的线段的结束点
        . double rho：double类型的rho，以像素为单位的距离精度
        . double theta: double类型的theta，以弧度为单位的角度精度
        . int threshold: int类型的threshold，累加平面的阈值参数，即识别某部分为图中的一条直线时它在累加平面中必须达到的值
        . double minLineLength: double类型的minLineLength，有默认值0，表示最低线段的长度，比这个设定参数短的线段就不能被显现出来
        . double maxLineGap: double类型的maxLineGap，有默认值0，允许将同一行点与点之间连接起来的最大的距离
    """
    linesp = cv.HoughLinesP(canny_mat, 1, np.pi / 180, 22, minLineLength = 10, maxLineGap = 10)
    # 画线
    for i in range(linesp.shape[0]):
        for j in range(linesp.shape[1]):
            p1 = (linesp[i, j, 0], linesp[i, j, 1])
            p2 = (linesp[i, j, 2], linesp[i, j, 3])
            cv.line(srcmat, p1, p2, (255, 255, 0), 1, 8, 0)
    
    cv.imshow("src", srcmat)
    cv.imshow("canny_mat", canny_mat)
    cv.waitKey(0)
