import cv2 as cv


# 第四周练习1 图像形态学
def morphology():
    srcmat = cv.imread("d:/coin.png")
    if srcmat is None:
        print("读取图片失败")
        return
    # 二值化
    ret, th_mat = cv.threshold(srcmat, 100, 255, cv.THRESH_BINARY)
    # 获取结构元素
    """
        getStructuringElement（） 函数模型：
        getStructuringElement(int shape, Size ksize, Point anchor = Point(-1,-1));
    
        参数介绍：
        . int shape: 这个函数的第一个参数表示内核的形状，有三种形状可以选择。矩形：MORPH_RECT;交叉形：MORPH_CROSS;椭圆形：MORPH_ELLIPSE;
        . Size ksize: 内核的尺寸
        . Point anchor: 锚点的位置
    """
    element = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    # 腐蚀
    """
    erode（） 函数模型：
         erode( InputArray src, OutputArray dst, InputArray kernel,
                             Point anchor = Point(-1,-1), int iterations = 1,
                             int borderType = BORDER_CONSTANT,
                             const Scalar& borderValue = morphologyDefaultBorderValue() );
    
        参数介绍：
        . InputArray src: Mat类，通道数量不限，但深度应为CV_8U,CV_16U...
        . OutputArray dst: 输出图像，需要有和原图片一样的尺寸和类型
        . InputArray kernel: 腐蚀操作的内核，一般用3*3的核
        . Point anchor:锚的位置，一般用（-1，-1）
        .int iterations:使用函数的次数
        .int borderType:用于推断图像外部像素的某种边界模式
        . const Scalar& borderValue:边界为常数时的边界值
    """
    erode_mat = cv.erode(th_mat, element)
    # 膨胀
    """
    dialte（） 函数模型：
        dilate( InputArray src, OutputArray dst, InputArray kernel,
                              Point anchor = Point(-1,-1), int iterations = 1,
                              int borderType = BORDER_CONSTANT,
                              const Scalar& borderValue = morphologyDefaultBorderValue() );
    
        参数介绍：
        . InputArray src: Mat类，通道数量不限，但深度应为CV_8U,CV_16U...
        . OutputArray dst: 输出图像，需要有和原图片一样的尺寸和类型
        . InputArray kernel: 腐蚀操作的内核，一般用3*3的核
        . Point anchor:锚的位置，一般用（-1，-1）
        .int iterations:使用函数的次数
        .int borderType:用于推断图像外部像素的某种边界模式
        . const Scalar& borderValue:边界为常数时的边界值
    """
    dilate_mat = cv.dilate(th_mat, element)
    
    """
    morphologyEx（） 函数模型：
         morphologyEx( InputArray src, OutputArray dst,
                                    int op, InputArray kernel,
                                    Point anchor = Point(-1,-1), int iterations = 1,
                                    int borderType = BORDER_CONSTANT,
                                    const Scalar& borderValue = morphologyDefaultBorderValue() );
    
    
        参数介绍：
        . InputArray src: Mat类，通道数量不限，但深度应为CV_8U,CV_16U...
        . OutputArray dst: 输出图像，需要有和原图片一样的尺寸和类型
        . int op:表示形态学运算的类型，如MORPH_OPEN、MORPH_CLOSE分别代表开运算和闭运算
        . InputArray kernel: 腐蚀操作的内核，一般用3*3的核
        . Point anchor:锚的位置，一般用（-1，-1）
        . int iterations:使用函数的次数
        . int borderType:用于推断图像外部像素的某种边界模式
        . const Scalar& borderValue:边界为常数时的边界值
    """
    # 开运算
    open_mat = cv.morphologyEx(th_mat, cv.MORPH_OPEN, element)
    # 闭运算
    close_mat = cv.morphologyEx(th_mat, cv.MORPH_CLOSE, element)
    
    # 显示图像
    cv.imshow("erode_mat", erode_mat)
    cv.imshow("dilate_mat", dilate_mat)
    cv.imshow("open_mat", open_mat)
    cv.imshow("dilate_mat", dilate_mat)
    cv.imshow("close_mat", close_mat)
    cv.waitKey(0)


# 第四周练习2：连通域标记
def conectedwithstats():
    # 读取照片
    srcmat = cv.imread("d:/coin.png")
    if srcmat is None:
        print("读取图像失败")
        return
    # 转化为灰度图
    grymat = cv.cvtColor(srcmat, cv.COLOR_BGR2GRAY)
    # 二值化
    ret, th_mat = cv.threshold(grymat, 100, 255, cv.THRESH_BINARY)
    # 获取结构元素
    element = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    # 膨胀
    dilate_mat = cv.dilate(th_mat, element, 2)
    # 进行连通域标记
    """""
    connectedComponentsWithStats（） 函数模型：
            connectedComponentsWithStats(InputArray image, OutputArray labels,
                                              OutputArray stats, OutputArray centroids,
                                              int connectivity = 8, int ltype = CV_32S)
            参数介绍：
            . InputArray image: 输入8位单通道二值图像
            . OutputArray labels: 输出和原图image一样大的标记图，label对应于表示是当前像素是第几个轮廓，背景置0
            . OutputArray stats:输出nccomps（标签数）×5的矩阵 ，表示每个连通区域的外接矩形和面积（pixel）
            . OutputArray centroids: 对应的是轮廓的中心点。nccomps×2的矩阵 表示每个连通区域的质心
            . int connectivity:使用8邻域或者4邻域
            . int ltype:输出标签的数据类型
    
    """
    nccomps = cv.connectedComponentsWithStats(dilate_mat)
    ncomp = nccomps[0]
    labels = nccomps[1]
    stats = nccomps[2]
    print(f"连通域个数为：{ncomp - 1}")
    # 对识别出的连通域加最小外接边框
    for i in range(ncomp):
        pt1 = (stats[i, 0], stats[i, 1])
        pt2 = (stats[i, 0] + stats[i, 2], stats[i, 1] + stats[i, 3])
        # 画外接矩形
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
        cv.rectangle(th_mat, pt1, pt2, 255, 1, 8, 0)
    cv.imshow("dilate_mat", dilate_mat)
    cv.imshow("th_mat", th_mat)
  
    
# 第四周练习3 原点计数
def origincount():
    srcmat = cv.imread("d:/1.jpg")
    if srcmat is None:
        print("读取图片失败")
        return
    grymat = cv.cvtColor(srcmat, cv.COLOR_BGR2GRAY)
    # 反色
    grymat = 255 - grymat
    # 二值化
    ret, th_mat = cv.threshold(grymat, 120, 255, cv.THRESH_BINARY)
    # 获取结构元素
    element = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
    # 腐蚀
    erode_mat = cv.erode(th_mat, element, 5)
    # 连通域标记
    
    nccomps = cv.connectedComponentsWithStats(erode_mat)
    num = nccomps[0] - 1
    print(f"原点个数为：{num}")
    cv.imshow("erode_mat", erode_mat)


# 第四周练习4 回型针计数
def clipcount():
    srcmat = cv.imread("d:/clip.png")
    if srcmat is None:
        print("读取图片失败")
        return
    # 灰度图转化
    gry_mat = cv.cvtColor(srcmat, cv.COLOR_BGR2GRAY)
    # 反色
    gry_mat = 255 - gry_mat
    # 二值化
    ret, th_mat = cv.threshold(gry_mat, 100, 255, cv.THRESH_BINARY)
    # 定义结构元素
    element = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    # 开运算
    open_mat = cv.morphologyEx(th_mat, cv.MORPH_OPEN, element)
    # 连通域标记
    nccomps = cv.connectedComponentsWithStats(open_mat)
    stats = nccomps[2]
    ncomp = nccomps[0]
    # 筛选连通域
    for i in range(nccomps[0]):
        width = stats[i, 2]
        height = stats[i, 3]
        ratio = int(height / width)
        if ratio > 10:
            ncomp -= 1
    print(f"回形针个数为：{ncomp - 1}")
    cv.imshow("open_mat", open_mat)
