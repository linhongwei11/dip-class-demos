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
    element = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    # 腐蚀
    erode_mat = cv.erode(th_mat, element)
    # 膨胀
    dilate_mat = cv.dilate(th_mat, element)
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
