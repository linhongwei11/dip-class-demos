import cv2 as cv
import numpy as np


# 第八周练习1 轮毂中的圆孔定位
def rimblobanalysis():
    wh_ratio_high = 1.1
    wh_ratio_low = 0.9
    area_th = 100
    srcmat = cv.imread("d:/rim.png")
    if srcmat is None:
        print("fail to read ")
        return
    # 转化为灰度图
    gry_mat = cv.cvtColor(srcmat, cv.COLOR_BGR2GRAY)
    # 二值化
    ret, th_mat = cv.threshold(gry_mat, 100, 255, cv.THRESH_BINARY)
    # 反色
    th_mat = 255 - th_mat
    # 定义结构元素
    element = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    # 进行闭运算
    close_mat = cv.morphologyEx(th_mat, cv.MORPH_CLOSE, element)
    # 连通域
    ncomps = cv.connectedComponentsWithStats(close_mat)
    # 提取连通域个数、标签
    ncomp = ncomps[0]
    labels = ncomps[1]
    stats = ncomps[2]
    # 新建数组，存放标签值
    flag = [0] * ncomp
    
    # 筛选连通域
    for i in range(ncomp):
        width = stats[i, 2]
        height = stats[i, 3]
        ratio = width / height
        area = stats[i, 4]
        if (ratio < wh_ratio_high) and (ratio > wh_ratio_low) and (area > area_th):
            flag[i] = 1
    
    # 给筛选出的像素区域上色
    for i in range(srcmat.shape[0]):
        for j in range(srcmat.shape[1]):
            if flag[labels[i, j]] == 1:
                srcmat[i, j, 0] = 0
                srcmat[i, j, 1] = 255
                srcmat[i, j, 2] = 255
    cv.imshow("close", close_mat)
    cv.imshow("src", srcmat)
    cv.waitKey(0)


# 第八周练习2 芯片定位
def chipblobanalysis():
    wh_ratio_high = 1.2
    wh_ratio_low = 0.9
    # 读取图像
    srcmat = cv.imread("d:/die_on_chip.png")
    dst_mat = srcmat.copy()
    gry_mat = cv.cvtColor(srcmat, cv.COLOR_BGR2GRAY)
    # 二值化
    ret, th_mat = cv.threshold(gry_mat, 100, 255, cv.THRESH_OTSU)
    # 获取结构元素
    element = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    # 腐蚀降噪
    erode_mat = cv.erode(th_mat, element)
    # 通过findContours函数寻找连通域
    """
        findContours（） 函数模型：
        findContours( InputOutputArray image, OutputArrayOfArrays contours,
                                  int mode, int method, Point offset = Point());
    
        参数介绍：
        . InputOutputArray image：image，单通道图像矩阵
        . OutputArrayOfArrays contours：contours，定义为“vector<vector<Point>> contours”，是一个向量，并且是一个双重向量
        . int mode：int型的mode，定义轮廓的检索模式
        . int method: 定义轮廓的近似方法
        . Point offset: Point偏移量，所有的轮廓信息相对于原始图像对应点的偏移量
    """
    contours, hierarchy = cv.findContours(erode_mat, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    for i in range(len(contours)):
        # 获取最小外接四边形
        rbox = cv.minAreaRect(contours[i])
        width, height = rbox[1]
        box = cv.boxPoints(rbox)
        box = np.int0(box)
        print(contours)
       
        # 计算宽长比
        if height == 0:
            ratio = 0
        else:
            ratio = float(width) / float(height)
        
        # 条件筛选
        if (ratio > wh_ratio_low) and (ratio < wh_ratio_high):
            # 绘制轮廓
            """
            drawContours（） 函数模型：
                drawContours( InputOutputArray image, InputArrayOfArrays contours,
                                  int contourIdx, const Scalar& color,
                                  int thickness = 1, int lineType = LINE_8,
                                  InputArray hierarchy = noArray(),
                                  int maxLevel = INT_MAX, Point offset = Point() );
    
                参数介绍：
                . InputOutputArray image：目标图像
                . InputArrayOfArrays contours：表示输入的轮廓组，每一组轮廓由点vector构成量
                . int contourIdx：指明画第几个轮廓，如果该参数为负值，则画全部轮廓
                . const Scalar& color: color为轮廓的颜色
                . int thickness: thickness为轮廓的线宽，如果为负值或CV_FILLED表示填充轮廓内部
                . int lineTyp:lineType为线型
                . InputArray hierarchy:轮廓结构信息
                . int maxLevel:maxLevel
                . Point offset:点偏移量
            """
            cv.drawContours(srcmat, contours, i, (0, 255, 255))
            cv.drawContours(dst_mat, [box], 0, (0, 0, 255), 2)
    cv.imshow("erodemat", erode_mat)
    cv.imshow("findContours_mat", srcmat)
    cv.imshow("img", dst_mat)


# 第八周练习3 杯盖检测
def cap_blob():
    # 肤色h
    i_minh = 0
    i_maxh = 20
    
    # 肤色h
    i_minh2 = 160
    i_maxh2 = 180
    
    # 颜色饱和度s
    i_mins = 100
    i_maxs = 255
    
    # 颜色亮度v
    i_minv = 50
    i_maxv = 255
    # 读取照片
    srcmat = cv.imread("d:/lib.JPG")
    # 判断是否读取成功
    if srcmat is None:
        print("pic fail to read")
        return
    # 转化图片为hsv格式
    hsv_mat = cv.cvtColor(srcmat, cv.COLOR_BGR2HSV)
    # 筛选出红色杯盖区域
    dst_mat1 = cv.inRange(hsv_mat, (i_minh, i_mins, i_minv), (i_maxh, i_maxs, i_maxv))
    dst_mat2 = cv.inRange(hsv_mat, (i_minh, i_mins, i_minv), (i_maxh, i_maxs, i_maxv))
    inrange_mat = dst_mat2 + dst_mat1
    # 进行膨胀运算
    element = cv.getStructuringElement(cv.MORPH_RECT, (33, 33))
    dialte_mat = cv.dilate(inrange_mat, element)
    # 获取连通域相关信息
    ncomps = cv.connectedComponentsWithStats(dialte_mat)
    # 得到连通域个数
    ncomp = ncomps[0]
    stats = ncomps[2]
    # 从非背景的第一个连通域开始循环
    for i in range(1, ncomp):
        # 分别得到像素总数，中心点，长宽等信息
        area = stats[i, 4]
        x = stats[i, 0]
        y = stats[i, 1]
        width = stats[i, 2]
        height = stats[i, 3]
        if area > 10000:
            # 画矩形
            cv.rectangle(srcmat, (x, y), (x + width, y + height), (0, 0, 255))
  
    cv.imshow("dialte_mat", dialte_mat)
    cv.imshow("srcmat", srcmat)
    cv.waitKey(0)
    cv.destroyAllWindows()
