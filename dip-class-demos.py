import cv2 as cv
import function

t1 = cv.getTickCount()
n = 10000
ifprint = True
# 读取图片
src = cv.imread("d:/timg.jpg")
# 通道分离函数
# function.image_split(src)
# 读取视频函数
function.readvideo()
# 画框
function.drawing(src)
grymat = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
# 求直方图
function.histogram(grymat)

t2 = cv.getTickCount()
# 计算函数运行时间
time_pickprime = (t2 - t1) / cv.getTickFrequency()
print("time:%s ms" % (time_pickprime * 1000))
cv.waitKey(0)
