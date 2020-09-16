import cv2 as cv
import math
import numpy as np


# 第9周练习 手动实现HOG比较图像相似度
# 手动实现HOG
def calhog(src, hist, nangle, cellsize):
    # 判断读取的尺寸是否正确
    if cellsize > src.shape[0] or cellsize > src.shape[1]:
        return -1
    # 参数设置
    nx = int(src.shape[1] / cellsize)
    ny = int(src.shape[0] / cellsize)
    binangle = 360 / nangle
    
    # 计算梯度及角度
    gx = cv.Sobel(src, cv.CV_32F, 1, 0)
    gy = cv.Sobel(src, cv.CV_32F, 0, 1)
    mag, angle = cv.cartToPolar(gx, gy)
    # 提取一个cell的梯度及长度
    for i in range(nx):
        for j in range(ny):
            roimag = mag[i * cellsize:(i + 1) * cellsize, j * cellsize:(j + 1) * cellsize]
            roiang = angle[i * cellsize:(i + 1) * cellsize, j * cellsize:(j + 1) * cellsize]
            h_head = (i * nx + j) * nangle
            for m in range(roimag.shape[0]):
                for n in range(roimag.shape[1]):
                    pos = int(roiang[m, n] / binangle)
                    hist[h_head + pos] = roimag[m, n] + hist[h_head + pos]
    return 0


# 计算直方图距离
def norml2(hist1, hist2, size):
    d_sum = 0
    for i in range(size):
        d_sum = d_sum + (hist1[i] - hist2[i]) * (hist1[i] - hist2[i])
    d_sum = math.sqrt(d_sum)
    return d_sum


# 比较三张图片
def compareimage():
    # 读取3张图片，并将其转化为灰度图
    ref_mat = cv.imread("d:/hogTemplate.jpg")
    ref_gry = cv.cvtColor(ref_mat, cv.COLOR_BGR2GRAY)
    pl_mat = cv.imread("d:/img1.jpg")
    pl_gry = cv.cvtColor(pl_mat, cv.COLOR_BGR2GRAY)
    bg_mat = cv.imread("d:/img2.jpg")
    bg_gry = cv.cvtColor(bg_mat, cv.COLOR_BGR2GRAY)
    
    # 参数设置
    nangle = 8
    blocksize = 16
    nx = int(ref_gry.shape[1] / blocksize)
    ny = int(ref_gry.shape[0] / blocksize)
    bins = nx * ny * nangle
    
    # 新建数组
    ref_hist = [0] * bins
    pl_hist = [0] * bins
    bg_hist = [0] * bins
    
    recode = calhog(ref_gry, ref_hist, nangle, blocksize)
    recode = calhog(pl_gry, pl_hist, nangle, blocksize)
    recode = calhog(bg_gry, bg_hist, nangle, blocksize)
    
    # 计算直方图距离
    dis1 = norml2(ref_hist, pl_hist, bins)
    dis2 = norml2(ref_hist, bg_hist, bins)
    
    print(f"distance between reference and img1:{dis1}")
    print(f"distance between reference and img2:{dis2}")
    
    # 比较直方图距离，输出结果
    if dis1 <= dis2:
        print("img1 is similar")
    else:
        print("img2 is similar")
    
    cv.imshow("ref", ref_gry)
    cv.imshow("img1", pl_gry)
    cv.imshow("img2", bg_mat)
    cv.waitKey(0)


# harris角点检测的使用
def harrisdetector():
    # 读取视频
    capture = cv.VideoCapture("d:/vtest.avi")
    # 参数设置
    blocksize = 2
    aperturesize = 3
    k = 0.04
    thresh = 200
    while True:
        # 读取一帧图片
        ret, frame = capture.read()
        cv.imshow("src",frame)

        # 转化为灰度图
        graymat = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        # 初始化图像
       
        """

              0.输入图像，单通道8位图像 or 浮点图像
              1.输出的相应Harris响应结果，类型为CV_32FC1
              2.计算特征值的窗口大小
              3.Sobel算子的窗口大小
              4.公式中的k值，详细见课件
              5.边缘处理

         """
        dst = cv.cornerHarris(graymat, blocksize, aperturesize, k, cv.BORDER_DEFAULT)
        # 归一化
        """
        normalize（） 函数模型：
        normalize( InputArray src, InputOutputArray dst, double alpha = 1, double beta = 0,
                                 int norm_type = NORM_L2, int dtype = -1, InputArray mask = noArray());
    
        参数介绍：
                InputArray src：输入数组
                InputOutputArray dst：输出数组，支持原地运算
                double alpha：range normalization模式的最小值
                double beta：range normalization模式的最大值，不用于norm normalization(范数归一化)模式。
                normType：归一化的类型，可以有以下的取值：
                          NORM_MINMAX:数组的数值被平移或缩放到一个指定的范围，线性归一化，一般较常用。
                          NORM_INF:此类型的定义没有查到，根据OpenCV 1的对应项，可能是归一化数组的C-范数(绝对值的最大值)
                          NORM_L1 : 归一化数组的L1-范数(绝对值的和)
                          NORM_L2: 归一化数组的(欧几里德)L2-范数
                dtype：dtype为负数时，输出数组的type与输入数组的type相同；否则，输出数组与输入数组只是通道数相同，而tpye=CV_MAT_DEPTH(dtype).
                mask：操作掩膜，用于指示函数是否仅仅对指定的元素进行操作
        """
        cv.normalize(dst, dst, 0, 255, cv.NORM_MINMAX, cv.CV_32FC1)
        
        # convertScaleAbs函数
        #  该函数实行3个功能，乘以尺度，取绝对值，转换至uchar类型的Mat
        # dst=saturate(alpha*src+beta)
        # 默认值alpha==1 beta==0
        # 故本例中实际就是转换为可显示的uchar类型
        dstnorm=cv.convertScaleAbs(dst)
        for i in range(dstnorm.shape[0]):
            for j in range(dstnorm.shape[1]):
                if int(dstnorm[i, j] > thresh):
                    cv.circle(dst, (i, j), 5, 0, 2, 8, 0)
        cv.imshow("corner", dstnorm)
        cv.waitKey(30)
