# 高级搜索解决旅行商问题

## 实验题目
使用模拟退火和遗传算法解决TSP问题
## 实验内容

### 模拟退火算法

#### 1.算法原理

模拟退火算法来源于固体退火原理，将固体加温至充分高，再让其徐徐冷却，加温时，固体内部粒子随温升变为无序状，内能增大，而徐徐冷却时粒子渐趋有序，在每个温度都达到平衡态，最后在常温时达到基态，内能减为最小。

#### 2.伪代码

(1) 初始化：初始温度T(充分大)，初始解状态S(是算法迭代的起点)，每个T值的迭代次数L

(2) 对k=1, …, L做第(3)至第6步：

(3) 产生新解S′

(4) 计算增量ΔT=C(S′)-C(S)，其中C(S)为评价函数

(5) 若ΔT<0则接受S′作为新的当前解，否则以概率exp(-ΔT/T)接受S′作为新的当前解.

(6) 如果满足终止条件则输出当前解作为最优解，结束程序。

终止条件通常取为连续若干个新解都没有被接受时终止算法。

(7) T逐渐减少，且T->0，然后转第2步。

#### 3.关键代码展示

##### 局部搜索策略

* 简单交换两个城市

  ```python
  def nextStatus_swap(self):
      temp=deepcopy(self.path)
      left = np.random.randint(0, self.dim - 1)
      right = np.random.randint(left + 1, self.dim)
      # 交换位置
      temp[left],temp[right]=temp[right],temp[left]
      return temp
  ```

* 交换城市并且翻转

  ```python
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
  ```

* 找到城市放到开头

  ```python
  # 随机找到两个点，要求两个点不能相同，提取该序列放到路径的头部
  def nextStatus_head(self):
      left = np.random.randint(0, self.dim - 1)
      right = np.random.randint(left + 1, self.dim)
      new_index=np.arange(left,right+1)
      new_index=np.append(new_index,np.delete(range(self.dim),new_index))
      return self.path[new_index]
  ```

##### 爬山法

未加入退火策略的随机算法

```python
def search_HC(self):
    t=self.t0
    while t>=self.te:
        for i in range(self.n):
            next_status=self.nextStatus_head()  # 获取下一个状态
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
```

##### 退火法

加入退火策略的随机算法

```python
def search_SA(self):
    t=self.t0
    while t>=self.te:
        for i in range(self.n):
            next_status=self.nextStatus_head()  # 获取下一个状态
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
```

#### 4.创新点

在创新点方面主要是尝试了多种局部搜索策略并尝试了爬山法与退火法进行对比，具体代码可以查看[关键代码展示](#3关键代码展示-1)

#### 5.优化与比较

##### 爬山法与退火法比较

测试集lin105，局部搜索方法:交换城市并且翻转

| 算法策略 | 最短距离 | 时间 | 结果                                                         |
| -------- | -------- | ---- | ------------------------------------------------------------ |
| 爬山法   | 15853.5  | 13.7 | <img src="D:\Programme\Python\TSP\lin105_HC_test.png" alt="lin105_HC_test" style="zoom:50%;" /> |
| 退火法   | 15023.2  | 14.1 | <img src="D:\Programme\Python\TSP\lin105_SA_test.png" alt="lin105_SA_test" style="zoom:50%;" /> |

通过比较可以发现爬山法收敛速度极快并陷入局部最优，退火法收敛速度较慢但没有陷入局部最优。另外在速度方面二者相差不多。

##### 局部搜索策略比较

测试集lin105

| 局部搜索策略     | 最短路径 | 时间   |
| ---------------- | -------- | ------ |
| 简单交换两个城市 | 18767.1  | 13.3   |
| 交换城市并且翻转 | 14723.3  | 14.9秒 |
| 找到城市放到开头 | 16423.1  | 21.9秒 |

从测试结果可以看出：第二种局部搜索策略更优。

#### 6.测试结果

| 测试集 | 最短路径 | 时间    | 效果图                                                       | 与最优解误差 |
| ------ | -------- | ------- | ------------------------------------------------------------ | ------------ |
| lin105 | 14919.5  | 14.5秒  | <img src="C:\Users\24293\AppData\Roaming\Typora\typora-user-images\image-20220507164316163.png" alt="image-20220507164316163" style="zoom:50%;" /> | 3.9%         |
| gr120  | 1744.4   | 15秒    | <img src="C:\Users\24293\AppData\Roaming\Typora\typora-user-images\image-20220507164802990.png" alt="image-20220507164802990" style="zoom:50%;" /> | 4.56%        |
| rd100  | 8059.9   | 13.75秒 | <img src="C:\Users\24293\AppData\Roaming\Typora\typora-user-images\image-20220507164614454.png" alt="image-20220507164614454" style="zoom:50%;" /> | 最优         |
| pr107  | 45120.6  | 15.2秒  | <img src="C:\Users\24293\AppData\Roaming\Typora\typora-user-images\image-20220507164521533.png" alt="image-20220507164521533" style="zoom:50%;" /> | 2.12%        |

从测试结果上来看，模拟退火表现优异，有一定的概率获得最优解。

### 遗传算法

#### 1.算法原理

遗传算法起源于对生物系统所进行的计算机模拟研究。它是模仿自然界生物进化机制发展起来的随机全局搜索和优化方法，借鉴了达尔文的进化论和孟德尔的遗传学说。其本质是一种高效、并行、全局搜索的方法，能在搜索过程中自动获取和积累有关搜索空间的知识，并自适应地控制搜索过程以求得最佳解。

#### 2.伪代码

1.评估每条染色体所对应个体的适应度。

2.遵照适应度越高，选择概率越大的原则，从种群中选择两个个体作为父方和母方。

3.抽取父母双方的染色体，进行交叉，产生子代。

4.对子代的染色体进行变异。

5.重复2，3，4步骤，直到新种群的产生或者迭代数结束。

#### 3.关键代码展示

##### 选择算子

* 轮盘赌策略：个体适应度越高，被选择的概率越大

  ``` python
    # 选择个体轮盘赌策略
      def select_roulette(self):
          fits=self.groupFitness()
          temp_group=np.array(self.group)
          new_group_index=np.random.choice(range(self.og),size=self.mc,replace=True,p=fits/fits.sum())
          # 轮盘赌选出相应个体的索引
          new_group=temp_group[new_group_index]  # 选出新个体
          self.group=new_group.tolist()
          self.og=self.mc
  ```

* 精英保留策略：依某种策略生成新种群后，用当代最优个体随机替换新种群的某个体，或者直接替换最差个体

  ``` python
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
  ```

* 截断选择策略：保留所有适应值在平均水平之上的个体

  ```python
  # 截断选择
  def select_truncation(self):
      fits=self.groupFitness()
      temp_index=[i for i,j in enumerate(fits>np.average(fits)) if j]
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
  ```

##### 交叉算子

* OX：这里采用了单点交叉

  ``` python
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
  ```

* PMX(**Partial-Mapped Crossover** ) 这里采用了双点交叉

  ```python
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
  ```

##### 变异算子

* 简单交换两个城市

  ``` python
  def mutate_swap(self):
      for i in range(self.og):
          if np.random.random()<self.pm:
              random_site0 = np.random.randint(0, self.dim-1)
              random_site1 = np.random.randint(random_site0,self.dim)
              # 交换两个城市
              self.group[i][random_site0], self.group[i][random_site1] = self.group[i][random_site1], self.group[i][random_site0]
  ```

* 交换城市并倒置

  ``` python
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
  ```

##### 其它

* 搜索函数

  ``` python
  def search(self):
      self.createOriginalGroup()
      for i in range(self.count):
          self.crossOver_OX()  # 交叉
          self.mutate_inversion()  # 变异
          self.select_optimal()  # 选择
          self.path,self.length=self.getOptimal()
          self.lengths.append(self.length)
  ```

#### 4.创新点

在创新点方面主要是尝试了多种选择算子、交叉算子、变异算子，具体代码可以查看[关键代码展示](#3关键代码展示-2)

#### 5.优化

在优化方面主要是通过反复测试训练集来选出最好的算子和相应的参数，下面给出了测试结果

**变异概率优化**：测试集lin105，进化数10000

| 变异概率 | 0.1   | 0.2   | 0.05 | 0.02|0.01|0.015|0.03|0.025| 0.022|
| -------- | ----- | ----- | ----- |----|----|----|-------|----|----|
| 最段路径 | 16283 | 32474| 15788 |15653|17090|16332|16241|16052|16008|

通过多方面的比较加上算法具有一定随机性的考量，这里选择变异概率0.05

下图给出0.05变异概率时的最优路径图。最短路径长:15526.3满足实验10%以内的要求。

<img src="D:\Programme\Python\TSP\lin105_trun.png" alt="image-20220506170243151" style="zoom:50%;" />

**交叉算子优化**：测试集lin105，进化数10000，交叉概率1，变异概率0.05，选择算子 精英选择策略

| 交叉算子   | PMX  |OX|
| ---- | ---- |----|
| 时间 |152秒|81秒|
| 最短路径| 15769| 15526|

可以看到交叉算子OX的性能明显优于PMX，故这里采用OX交叉算子进行下一步测试

**交叉概率优化**：测试集lin105，进化数10000，交叉概率1，变异概率0.05，交叉算子:OX，选择算子:精英选择策略

| 交叉概率 | 0.9   | 0.8   | 0.95  |
| -------- | ----- | ----- | ----- |
| 最短路径 | 15420 | 15928 | 15913 |
| 时间     | 72秒  | 67秒  | 75秒  |

从表中数据可以看出，当交叉概率为0.9时，遗传算法的效果和效率都表现优秀，故采用0.9

**选择算子优化**：测试集lin105，进化数10000，交叉概率1，变异概率0.05，交叉算子:OX

| 选择算子 | 轮盘赌策略 | 精英保留策略 |
| -------- | ---------- | ------------ |
| 最短路径 | 114093.2   | 14938.5      |
| 时间     | 65.3秒     | 66.8秒       |

由于截断选择需要大量的新个体产生，与此时的测试环境不符，故不对截断选择进行测试。

从表中数据可以看出轮盘赌策略效果很差，故采用精英保留策略。

#### 6.测试结果

| 测试集 | 最短路径 | 时间    | 效果图                                                       | 与最优解误差 |
| ------ | -------- | ------- | ------------------------------------------------------------ | ------------ |
| lin105 | 14938.5  | 66.8秒  | <img src="D:\Programme\Python\TSP\lin105_test.png" alt="image-20220507120318145" style="zoom:50%;" /> | 3.88%        |
| gr120  | 1788.1   | 73.6秒  | <img src="C:\Users\24293\AppData\Roaming\Typora\typora-user-images\image-20220507121000362.png" alt="image-20220507121000362" style="zoom:50%;" /> | 5.11%        |
| rd100  | 8684.9   | 113.4秒 | <img src="C:\Users\24293\AppData\Roaming\Typora\typora-user-images\image-20220507123657696.png" alt="image-20220507123657696" style="zoom:50%;" /> | 9.78%        |
| pr107  | 46096.6  | 64.8秒  | <img src="C:\Users\24293\AppData\Roaming\Typora\typora-user-images\image-20220507130029392.png" alt="image-20220507130029392" style="zoom:50%;" /> | 4.04%        |

通过测试结果可以发现优化后的GA算法表现优良，保证了最短路径长在最优解的10%以内。



### 实验结果

路径可视化：由于路径可视化会严重拖慢运行速度，所以在计算最短路时并没有实现路径可视化，而是将可视化功能放在计算完之后展示。

由于遍历数过于庞大，可视化时间过长，在这里就不予以展示，有兴趣可以直接运行程序查看。



