import cv2 as cv
import numpy as np

global img
img = cv.imread("d:/timg.jpg")
global mousecounter
mousecounter = []


# 回调函数
def on_mouse(event, x, y, flags, param):
    img1 = img.copy()
    # 当按下左键时
    if event == cv.EVENT_LBUTTONDOWN:
        point = (x, y)
        # 存储点坐标
        mousecounter.append([x, y])
        # 画出鼠标点击的位置
        cv.circle(img1, point, 4, (0, 255, 0), -1)
        cv.imshow("mousecallback", img1)


# 鼠标选择ROI区域
def selectpolygon(srcmat):
    # 初始化m
    m = np.zeros([srcmat.shape[0], srcmat.shape[1]], np.float32)
    if srcmat is None:
        print("fail to read image")
        return -1
    else:
        selectmat = srcmat.copy()
        dstmat = srcmat.copy()
    cv.namedWindow("mousecallback")
    cv.imshow("mousecallback", selectmat)
    # 回调函数
    cv.setMouseCallback("mousecallback", on_mouse)
    cv.waitKey(0)
    
    pts = np.array([mousecounter], np.int32)
    # 填充鼠标画出的区域
    m = cv.fillPoly(m, [pts], 255)
    dstmat = m.copy()
    # 返回结果
    return dstmat


# 鼠标响应的应用
def mousroi():
    # 读取图片
    srcmat = cv.imread("d:/timg.jpg")
    dstmat = srcmat.copy()
    # 调用前面定义的鼠标选择区域的函数
    dstmat = selectpolygon(srcmat)
    # 显示原图和结果
    cv.imshow("src", srcmat)
    cv.imshow("result", dstmat)
    cv.waitKey(0)
    return 0


# 输入一张图片将其转化为傅里叶变化后的幅值谱
def calvisibalmag(srcmat):
    gry_mat = cv.cvtColor(srcmat, cv.COLOR_BGR2GRAY)
    # 当图像的尺寸为2,3,5整数倍时，离散傅里叶变换的计算速度最快
    m = cv.getOptimalDFTSize(gry_mat.shape[0])
    n = cv.getOptimalDFTSize(gry_mat.shape[1])
    # 扩展边界
    padmat = cv.copyMakeBorder(gry_mat, 0, m - gry_mat.shape[0], 0, n - gry_mat.shape[1], cv.BORDER_CONSTANT, 0)
    planes = [padmat.astype(np.float32), np.zeros([padmat.shape[0], padmat.shape[1]], np.float32)]
    # 合并为多通道图像
    complexmat = cv.merge([planes[0], planes[1]])
    # 进行傅里叶变换
    complexmat = cv.dft(complexmat)
    # 分离双通道的图像，通道1存实部，通道2存虚部
    planes = cv.split(complexmat)
    # 求相位，保存在planes[0]中
    planes[0] = cv.magnitude(planes[0], planes[1])
    magmat = planes[0]
    # 将低频部分移到图像中心
    magmat = np.fft.fftshift(magmat)
    # 图像求对数
    magmat = np.log(1 + np.abs(magmat))
    # 图像数值归一化
    cv.normalize(magmat, magmat, 0, 1, cv.NORM_MINMAX)
    # magmat=magmat*255
    return magmat


# 傅里叶变换
def defdemo():
    # 读取图像
    srcmat = cv.imread("d:/timg.jpg")
    
    # 转化为灰度图
    gry_mat = cv.cvtColor(srcmat, cv.COLOR_BGR2GRAY)
    # 调用傅里叶计算函数
    magmat = calvisibalmag(srcmat)
    cv.imshow("srcmat", srcmat)
    cv.imshow("input image", magmat)
    cv.waitKey(0)


# 傅里叶逆变换函数
def iffdemo():
    # 读取原图，并转化为灰度图
    srcmat = cv.imread("d:/timg.jpg", 0)
    # 傅里叶变换
    dft_mat = cv.dft(np.float32(srcmat), flags = cv.DFT_COMPLEX_OUTPUT)
    # 得到频谱图
    dft = (np.log(cv.magnitude(dft_mat[:, :, 0], dft_mat[:, :, 1])))
    # 归一化
    cv.normalize(dft, dft, 0, 1, cv.NORM_MINMAX)
    # 将低频部分移到图像中心
    dft_shift_mat = np.fft.fftshift(dft_mat)
    # 得到频谱图
    dft_shift = np.log(cv.magnitude(dft_shift_mat[:, :, 0], dft_shift_mat[:, :, 1]))
    cv.normalize(dft_shift, dft_shift, 0, 1, cv.NORM_MINMAX)
    # 将低频部分移到图像边缘
    idft_shift_mat = np.fft.ifftshift(dft_shift_mat)
    # 傅里叶反变换
    idft = cv.idft(idft_shift_mat)
    # 转化为图像
    idft = cv.magnitude(idft[:, :, 0], idft[:, :, 1])
    cv.normalize(idft, idft, 0, 1, cv.NORM_MINMAX)
    
    cv.imshow("dft", dft)
    cv.imshow("srcmat", srcmat)
    cv.imshow(" dft_shift", dft_shift)
    cv.imshow("result", idft)
    cv.waitKey(0)
