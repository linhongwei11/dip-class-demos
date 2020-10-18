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
        """
            cvTColor（） 函数模型：
                cvtColor( InputArray src, OutputArray dst, int code, int dstCn = 0 );
    
                参数介绍：
                . InputArray src: 输入图像即要进行颜色空间变换的原图像，可以是Mat类
                . OutputArray dst: 输出图像即进行颜色空间变换后存储图像，也可以Mat类
                . int code: 转换的代码或标识，即在此确定将什么制式的图片转换成什么制式的图片，
                . int dstCn = 0: 目标图像通道数，如果取值为0，则由src和code决定
        """
        # 将图像转化为hsv
        hsv_mat = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        """
        inRange（） 函数模型：
                inRange(InputArray src, InputArray lowerb, InputArray upperb, OutputArray dst)；
    
                参数介绍：
                . InputArray src: 输入要处理的图像，可以为单通道或多通道
                . InputArray lowerb: 包含下边界的数组或标量
                . InputArray upperb: 包含上边界数组或标量
                . OutputArray dst: 输出图像，与输入图像src 尺寸相同且为CV_8U 类型
        """
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
    """
    threshold（） 函数模型：
        threshold(InputArray src, OutputArray dst, double thresh, double maxval, int type)；
    
        参数介绍：
        . InputArray src: 输入要处理的图像，可以为单通道或多通道
        . OutputArray dst: 输出图像，与输入图像src 尺寸相同且为CV_8U 类型
        . double thresh:阈值
        . double maxval:输出图像最大值
        . int type:阈值类型
                0: THRESH_BINARY  当前点值大于阈值时，取Maxval,否则设置为0
                1: THRESH_BINARY_INV 当前点值大于阈值时，设置为0，否则设置为Maxval
                2: THRESH_TRUNC 当前点值大于阈值时，设置为阈值，否则不改变
                3: THRESH_TOZERO 当前点值大于阈值时，不改变，否则设置为0
                4: THRESH_TOZERO_INV  当前点值大于阈值时，设置为0，否则不改变
                ...
                8:THRESH_OTSU  通过大津法求出最佳阈值，大于阈值置255，小于置0
    """
    # 普通图像二值化
    ret, bin_mat = cv.threshold(gry_mat, 100, 255, cv.THRESH_BINARY)
    # 大津法图像二值化
    ret2, otsu_mat = cv.threshold(gry_mat, 100, 255, cv.THRESH_OTSU)
    """
        adaptiveThreshold（） 函数模型：
        adaptiveThreshold( InputArray src, OutputArray dst,double maxValue, int adaptiveMethod,int thresholdType, int blockSize, double C );
    
        参数介绍：
        . 参数1：InputArray类型的src，输入图像，填单通道，单8位浮点类型Mat即可。
        . 参数2：函数运算后的结果存放在这。即为输出图像（与输入图像同样的尺寸和类型）。
        . 参数3：预设满足条件的最大值。
        . 参数4：指定自适应阈值算法。可选择ADAPTIVE_THRESH_MEAN_C 或 ADAPTIVE_THRESH_GAUSSIAN_C两种。
        . 参数5：指定阈值类型。可选择THRESH_BINARY或者THRESH_BINARY_INV两种。（即二进制阈值或反二进制阈值）。
        . 参数6：表示邻域块大小，用来计算区域阈值，一般选择为3、5、7......等。
        . 参数7：参数C表示与算法有关的参数，它是一个从均值或加权均值提取的常数，可以是负数。

    """
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
    """"
    createTrackbar（） 函数模型：
        createTrackbar(const String& trackbarname, const String& winname,
                                  int* value, int count,
                                  TrackbarCallback onChange = 0,
                                  void* userdata = 0);

        参数介绍：
        . 参数1：const String&类型的trackbarname，用来代表轨迹条的名字
        . 参数2：onst String&类型的winname,滑动空间用于依附的图像窗口的名称。
        . 参数3：int* 类型的value，初始化阈值。
        . 参数4：int类型count，滑动空间的刻度范围。
        . 参数5： TrackbarCallback类型的onChange，这是一个指向回调函数的指针。
        . 参数6：void* 类型的userdata，用户传给回调函数的数据，用来处理轨迹条事件。
    """
    # 创建滑动条
    cv.createTrackbar("value", "image", 0, 255, callback)
    cv.waitKey(0)
