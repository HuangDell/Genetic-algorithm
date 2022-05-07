import copy
import numpy as np
from copy import deepcopy
class GA:
    def __init__(self,distmat):
        self.distmat=distmat  # 距离矩阵
        self.dim=distmat.shape[0]  # 维度
        self.og=50  # 种群数目
        self.group=[]  # 种群
        self.path=None
        self.length=0
        self.lengths=[]
        self.pc=0.9  # 交叉概率
        self.pm=0.05  # 变异概率
        self.count=10000  # 迭代数
        self.mc=self.og  # 种群中至少个体数
        pass

    def search(self):
        self.createOriginalGroup()
        for i in range(self.count):
            self.crossOver_OX()  # 交叉
            self.mutate_inversion()  # 变异
            self.select_optimal()  # 选择
            self.path,self.length=self.getOptimal()
            self.lengths.append(self.length)

    # 产生初始种群
    def createOriginalGroup(self):
        origin=[i for i in range(self.dim)]
        for i in range(self.og):
            person=np.random.permutation(origin)
            if person.tostring():
                self.group.append(np.random.permutation(origin))  # 产生随机个体

    # 个体适应值函数
    def fitness(self,status):
        return 1000/self.calDistance(status)

    # 获得种群中的所有个体的适应值和总和
    def groupFitness(self):
        fits=np.zeros(self.og)
        for i in range(self.og):
            fits[i]=self.fitness(self.group[i])
            pass
        return fits

    # 选择个体轮盘赌策略
    def select_roulette(self):
        fits=self.groupFitness()
        temp_group=np.array(self.group)
        new_group_index=np.random.choice(range(self.og),size=self.mc,replace=True,p=fits/fits.sum())
        # 轮盘赌选出相应个体的索引
        new_group=temp_group[new_group_index]  # 选出新个体
        self.group=new_group.tolist()
        self.og=self.mc

    # 精英保留策略
    def select_optimal(self):
        fits=self.groupFitness()
        temp_group=np.array(self.group)
        new_group_index=np.random.choice(self.og,size=self.mc,replace=True,p=fits/fits.sum())
        # 先进行轮盘赌策略筛选个体
        new_group=temp_group[new_group_index]
        new_fits=fits[new_group_index]
        max_fit=fits.argmax()
        min_fit=new_fits.argmin()
        new_group[min_fit]=temp_group[max_fit]  # 最优个体替换
        self.group=new_group.tolist()
        self.og=self.mc
        pass

    # 截断选择
    def select_truncation(self):
        fits=self.groupFitness()
        temp_index=[i for i,j in enumerate(fits>=np.average(fits)) if j]
        temp_group=np.array(self.group)
        temp_fits=fits[temp_index]
        temp_group=temp_group[temp_index]  # temp_group中是全部大于平均值的个体
        new_group_index=np.random.choice(len(temp_group),size=self.mc,replace=True,p=temp_fits/temp_fits.sum())
        new_group=temp_group[new_group_index]
        new_fits=temp_fits[new_group_index]
        max_fit=temp_fits.argmax()  # 同时保留精英
        min_fit=new_fits.argmin()
        new_group[min_fit]=temp_group[max_fit]
        self.group=new_group.tolist()
        self.og=self.mc
        pass


    def getOptimal(self):
        fits=self.groupFitness()
        return self.group[fits.argmax()],1000/np.max(fits)

    # 交叉
    def crossOver(self):
        temp=self.og
        for i in range(temp-1):
            if np.random.random()>self.pc:  # 判断是否交叉
                continue
            j=np.random.randint(i,temp)
            oops0=np.random.randint(0,self.dim-1)
            oops1=np.random.randint(oops0+1,self.dim)
            x,y=deepcopy(self.group[i]),deepcopy(self.group[j])
            x_hash=[k for k in y if k not in x[oops0:oops1]]
            y_hash=[k for k in x if k not in y[oops0:oops1]]
            k,m=0,0
            while k<self.dim:
                if oops0 == k:
                    k=oops1
                x[k]=x_hash[m]
                y[k]=y_hash[m]
                k+=1
                m+=1
            self.group.append(x)
            self.group.append(y)
            self.og+=2


    def crossOver_OX(self):
        temp=self.og
        for i in range(temp // 2):
            if np.random.random()>self.pc:  # 判断是否交叉
                continue
            parent1 = self.group[i]
            parent2 = self.group[i + temp // 2]
            oops = np.random.randint(1, self.dim)
            child1, child2 = list(parent1[:oops].copy()), list(parent2[:oops].copy())
            for j in range(len(parent1)):  # 解决冲突
                if parent1[j] not in child2:
                    child2.append(parent1[j])
                if parent2[j] not in child1:
                    child1.append(parent2[j])
            self.group.append(child1.copy())
            self.group.append(child2.copy())
            self.og+=2


    def crossOver_PMX(self):
        temp=self.og
        for n in range(temp//2):
            if np.random.random()>self.pc:  # 判断是否交叉
                continue
            parent1 = np.array(self.group[n])
            parent2 = np.array(self.group[n + temp // 2])
            child1,child2=copy.deepcopy(parent1),copy.deepcopy(parent2)
            oops0=np.random.randint(0,self.dim-1)
            oops1=np.random.randint(oops0+1,self.dim)
            cross_area=range(oops0,oops1)  # 交叉区索引
            keep_area=np.delete(range(self.dim),cross_area)  # 非交叉区索引
            keep1=parent1[keep_area]
            keep2=parent2[keep_area]
            cross1=parent1[cross_area]
            cross2=parent2[cross_area]
            child1[cross_area],child2[cross_area]=cross2,cross1  # 先对交叉区进行交换
            mapping=[[],[]]  # 映射表
            # 生成映射表
            for i, j in zip(cross1, cross2):
                if j in cross1 and i not in cross2:
                    index = np.argwhere(cross1 == j)[0, 0]
                    value = cross2[index]
                    while value in cross1:
                        index = np.argwhere(cross1 == value)[0, 0]
                        value = cross2[index]
                    mapping[0].append(i)
                    mapping[1].append(value)
                elif j not in cross1 and i not in cross2:
                    mapping[0].append(i)
                    mapping[1].append(j)
            # 根据映射表解决冲突
            for i, j in zip(mapping[0], mapping[1]):
                if i in keep1:
                    keep1[np.argwhere(keep1 == i)[0, 0]] = j
                elif i in keep2:
                    keep2[np.argwhere(keep2 == i)[0, 0]] = j
                if j in keep1:
                    keep1[np.argwhere(keep1 == j)[0, 0]] = i
                elif j in keep2:
                    keep2[np.argwhere(keep2 == j)[0, 0]] = i
            child1[keep_area], child2[keep_area] = keep1, keep2
            self.group.append(child1)
            self.group.append(child2)
            self.og+=2
        pass

    def mutate_swap(self):
        for i in range(self.og):
            if np.random.random()<self.pm:
                random_site0 = np.random.randint(0, self.dim-1)
                random_site1 = np.random.randint(random_site0,self.dim)
                # 交换两个城市
                self.group[i][random_site0], self.group[i][random_site1] = self.group[i][random_site1], self.group[i][random_site0]

    def mutate_inversion(self):
        for i in range(self.og):
            if np.random.random()<self.pm:
                random_site0 = np.random.randint(0, self.dim-1)
                random_site1 = np.random.randint(random_site0,self.dim)
                # 交换两个城市并将之间的城市倒置
                while random_site0 < random_site1:
                    self.group[i][random_site0],self.group[i][random_site1]=self.group[i][random_site1],self.group[i][random_site0]
                    random_site0+=1
                    random_site1-=1

    # 根据距离矩阵计算距离值
    def calDistance(self,status):
        dis=0
        for i in range(self.dim-1):
            dis+=self.distmat[status[i],status[i+1]]
        dis+=self.distmat[status[0],status[-1]]
        return dis
