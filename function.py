import math
import numpy as np


# 筛选2-n范围内的所有质数，并打印至状态栏
def pickprime(maxval, ifprint):
    print("pick out prime by trial division algorithm ")
    # 筛选2-n范围内的质数
    num_sum = 0
    for i in range(2, maxval):
        if isprime(i):
            if ifprint:
                print(f"{i} ", end="")
            num_sum += 1
            # 每20个换行
            if num_sum % 20 == 0:
                print("")
    print("")
    print(f"the sum of prime is:{num_sum}")
    
    
# 试除法检查质数
# 假设有自然数x，如需要确定x是否为质数，只需确定x能否被2到√x范围内的奇数整除
def isprime(number):
    sqrt_number = math.ceil(math.sqrt(number))+1
    # 1及负数不为质数
    if number < 2:
        return False
    # 2为最小质数
    elif number == 2:
        return True
    # 偶数必不为质数
    elif number % 2 == 0:
        return False
    else:
        # 确定能否被2到√x范围内的奇数整除
        for i in range(3, sqrt_number, 2):
            if number % i == 0:
                return False        
            return True


def eratossieve(maxval,ifprint):
    print("pick out prime by Eratosthenes's algorithm:")
    flag = [True] * (maxval + 1)
    flag[0] = False
    flag[1] = False
    num_sum = 0
    for i in range(2,maxval+1):
        # 如果第i号为质数
        if flag[i]:
            if ifprint:
                print(f"{i} ", end ="")
            num_sum += 1
            # 每20个换行
            if num_sum % 20 == 0:
                print("")
            for j in range(i, maxval + 1, i):
                flag[j] = False
    print(f"the sum of prime is{num_sum}")
    
    
    

    
    
    
        
        
    
    
