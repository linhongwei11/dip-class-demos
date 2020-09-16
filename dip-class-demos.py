import cv2 as cv
import function


t1 = cv.getTickCount()
n = 10000
ifprint = True
# function.skinrecognition()
# function.binarization()
function.trackbar()

t2 = cv.getTickCount()
# 计算函数运行时间
time_pickprime = (t2 - t1) / cv.getTickFrequency()
print("time:%s ms" % (time_pickprime * 1000))

cv.waitKey(0)