import cv2 as cv
import function

# 读取视频
function.readvideo()

# 读取图片
srcmat = cv.imread("d:/timg.jpg")
function.readimg(srcmat)

# 利用numpy创建图片
function.creat_image()

# 遍历所有像素点，并转化为灰度图
src = cv.imread("d:/timg.jpg")
function.traverse(src)
cv.waitKey(0)
