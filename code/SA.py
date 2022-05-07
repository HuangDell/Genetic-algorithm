# 模拟退火算法
import random
import numpy as np
import math
from copy import deepcopy
class SA:
    def __init__(self,distmat):
        self.t0=500.0  # 起始温度
        self.te=1.0  # 结束温度
        self.n=500  # 马尔可夫链长
        self.count=0
        self.q=0.99  # 降温速率
        self.distmat=distmat  # 距离矩阵
        self.dim=distmat.shape[0]  # 矩阵维度
        self.lengths=[]
        self.path=np.random.permutation([i for i in range(self.dim)])  # 先产生随机解
        self.paths=[]
        self.length=self.calDistance(self.path)  # 计算随机解的路径长
        pass

    def search(self):
        self.search_SA()

    # 根据距离矩阵计算距离值
    def calDistance(self,status):
        dis=0
        for i in range(self.dim-1):
            dis+=self.distmat[status[i],status[i+1]]
        dis+=self.distmat[status[0],status[-1]]
        return dis

    def nextStatus_inversion(self):  # 随机产生下一个状态
        temp=deepcopy(self.path)
        left = np.random.randint(0, self.dim - 1)
        right = np.random.randint(left + 1, self.dim)
        # 交换位置
        while left < right:
            temp[left],temp[right]=temp[right],temp[left]
            left+=1
            right-=1
        return temp

    # 随机找到两个点，要求两个点不能相同，提取该序列放到路径的头部
    def nextStatus_head(self):
        left = np.random.randint(0, self.dim - 1)
        right = np.random.randint(left + 1, self.dim)
        new_index=np.arange(left,right+1)
        new_index=np.append(new_index,np.delete(range(self.dim),new_index))
        return self.path[new_index]



    def nextStatus_swap(self):
        temp=deepcopy(self.path)
        left = np.random.randint(0, self.dim - 1)
        right = np.random.randint(left + 1, self.dim)
        # 交换位置
        temp[left],temp[right]=temp[right],temp[left]
        return temp


    def search_SA(self):
        t=self.t0
        while t>=self.te:
            for i in range(self.n):
                self.paths.append(self.path)
                next_status=self.nextStatus_inversion()  # 获取下一个状态
                next_distance=self.calDistance(next_status)  # 计算下一个状态的路径长
                df=next_distance-self.length
                # 是否接受解
                if df<0:
                    self.length=next_distance
                    self.path=next_status
                else:
                    p=math.exp(-df/t)
                    if p>=random.random():  # 不优于当前解也有一定机率接受
                        self.length=next_distance
                        self.path=next_status
                self.lengths.append(self.length)
                self.count+=1
            t*=self.q

    def search_HC(self):
        t=self.t0
        while t>=self.te:
            for i in range(self.n):
                next_status=self.nextStatus_inversion()  # 获取下一个状态
                next_distance=self.calDistance(next_status)  # 计算下一个状态的路径长
                df=next_distance-self.length
                # 是否接受解
                if df<0:  # 必须优于当前的解才会接受
                    self.length=next_distance
                    self.path=next_status
                self.lengths.append(self.length)
                self.count+=1
            t*=self.q
        pass


