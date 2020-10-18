import cv2 as cv


# 第五周练习1-3
def filtermat():
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("无法读取视频")
        return
    ret, frame = cap.read()
    if ret:
        # 中值滤波
        """
        medianBlur（） 函数模型：
        medianBlur( InputArray src, OutputArray dst, int ksize );
    
        参数介绍：
        . InputArray src：InputArray类型的src，可以是多通道的Mat类型的图像；但深度应CV_8U，CV_16U，CV_16S，CV_32F
        . OutputArray dst：OutputArray类型的dst，即目标图像，函数的输出参数，需要和源图片有一样的尺寸和类型。
        . int ksize：int类型的ksize，孔径的线性尺寸（aperture linear size），注意这个参数必须是大于1的奇数
        """
        median_mat = cv.medianBlur(frame, 3)
        # 均值滤波
        """
        blur（） 函数模型：
        blur( InputArray src, OutputArray dst,
                            Size ksize, Point anchor = Point(-1,-1),
                            int borderType = BORDER_DEFAULT );
    
    
        参数介绍：
        . InputArray src:InputArray类型的src，可以是多通道的Mat类型的图像；但深度应CV_8U，CV_16U，CV_16S，CV_32F
        . OutputArray dst:OutputArray类型的dst，即目标图像，函数的输出参数，需要和源图片有一样的尺寸和类型。
        . Size ksize:Size类型的ksize，内核的大小
        . Point anchor:Point类型的anchor，表示锚点
        . int borderType: int类型的borderType，用于推断图像外部像素的某种边界模式
        """
        blur_mat = cv.blur(frame, (3, 3))
        # 高斯滤波
        """
        GaussianBlur（） 函数模型：
        GaussianBlur( InputArray src, OutputArray dst, Size ksize,
                                    double sigmaX, double sigmaY = 0,
                                    int borderType = BORDER_DEFAULT );
    
        参数介绍：
        . InputArray src：InputArray类型的src，可以是多通道的Mat类型的图像；但深度应CV_8U，CV_16U，CV_16S，CV_32F
        . OutputArray dst：OutputArray类型的dst，即目标图像，函数的输出参数，需要和源图片有一样的尺寸和类型。
        . Size ksize：高斯核大小
        . double sigmaX, double sigmaY：X,Y方向上的高斯核标准偏差
        . int borderType：int类型的borderType，用于推断图像外部像素的某种边界模式
        """
        guass_mat = cv.GaussianBlur(frame, (3, 3), 1, 0)
        
        # 显示图片
        cv.imshow("median", median_mat)
        cv.imshow("blur", blur_mat)
        cv.imshow("guass", guass_mat)
        cv.waitKey(0)


# 第五周；练习4边缘提取
def sobel_extraction():
    
    # 读取摄像头
    capture=cv.VideoCapture(0)
    if not capture.isOpened():
        print("打开摄像头失败")
        return
    
    # 读取当前帧照片
    ret, frame = capture.read()
    # 利用sobel算子进行边缘提取
    """
    sobel（） 函数模型：
        Sobel( InputArray src, OutputArray dst, int ddepth,
                             int dx, int dy, int ksize = 3,
                             double scale = 1, double delta = 0,
                             int borderType = BORDER_DEFAULT );
    
        参数介绍：
        . InputArray src：InputArray 类型的src，为输入图像，填Mat类型即可
        . OutputArray dst：OutputArray类型的dst，即目标图像，函数的输出参数，需要和源图片有一样的尺寸和类型。
        . int ddepth：int类型的ddepth，输出图像的深度
        . int dx, int dy：X,Y方向上的差分阶数
        . int ksize：sobel核的大小
        . double scale：double类型的scale，计算导数值时可选的缩放因子，默认值是1
        . double delta: double类型的delta，表示在结果存入目标图（第二个参数dst）之前可选的delta值，有默认值0
        . int borderType：int类型的borderType，边界模式
    """
    sobel_mat = cv.Sobel(frame, -1, 1, 0, 5)
    cv.imshow("sobel", sobel_mat)
    
    
# 第五周练习5 磨皮程序
def convolution_app():
    cap = cv.VideoCapture(0)
    
    # 肤色h
    i_minh = 0
    i_maxh = 20
    
    # 颜色饱和度s
    i_mins = 43
    i_maxs = 255
    
    # 颜色亮度v
    i_minv = 55
    i_maxv = 255
    
    # 读取当前帧图片
    ret, frame = cap.read()
    
    # 转化为HSV图片
    hsvmat = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    
    # 筛选目标区域
    mask_mat = cv.inRange(hsvmat, (i_minh, i_mins, i_minv), (i_maxh, i_maxs, i_maxv))
    
    # 对原图进行高斯滤波
    guass_mat = cv.GaussianBlur(frame, (5, 5), 3, 0)
    
    # 滤波后图像与目标区域进行与操作，筛选出磨皮后的人脸
    img1_mat = cv.bitwise_and(guass_mat, guass_mat, mask = mask_mat)
    
    # 对目标区域进行反色
    mask_mat = 255 - mask_mat
    
    # 在原图上留出目标区域地方（为磨皮后的人脸腾地方）
    img2_mat = cv.bitwise_and(frame, frame, mask = mask_mat)
    
    # 将磨皮后的人脸放到原人像上
    object_mat = cv.add(img1_mat, img2_mat)
    
    # 显示图片
    cv.imshow("frame", frame)
    cv.imshow("img1_mat", img1_mat)
    cv.imshow("img2_mat", img2_mat)
    cv.imshow("mask", mask_mat)
    cv.imshow("ob", object_mat)
