import time

import numpy as np
from SA import SA
from GA import GA
import DrawPath
fileName=['lin105.tsp','bays29.tsp','bays10.tsp','pr107.tsp','att48.tsp','gr120.tsp','u159.tsp','rd100.tsp']
# 22436.2366
def getOriginalData(choose:int):
    with open(fileName[choose]) as fp:
        lines=fp.readlines()
        name,dim=lines[0].split(' ')[-1],int(lines[3].split(' ')[-1])
        graph=np.zeros((dim,3))  # 0:city index 1:x 2:y
        distmat=np.zeros((dim,dim))
        for i in range(dim):
            for j,pox in enumerate(filter(lambda x: x and x.strip(),lines[i+6].split(' '))):
                graph[i][j]=float(pox)
        for i in range(dim):
            for j in range(i,dim):
                if i==j:
                    distmat[i][j]=float('inf')
                else:
                    distmat[i][j]=distmat[j][i]=np.linalg.norm(graph[i,1:]-graph[j,1:])
        return name,graph,distmat

def start():
    print("1.SA\t2.GA")
    alg_choose=int(input())
    print("1.lin105\t2.bays29\t3.bays10")
    print("4.pr107 \t5.att48 \t6.gr120")
    print("7.u159   \t8.rd100")
    choose=int(input())
    choose-=1
    if choose>=len(fileName):
        return
    name,graph,distmat=getOriginalData(choose)
    if alg_choose==1:
        alg=SA(distmat)
    else:
        alg=GA(distmat)
    start=time.process_time()
    alg.search()
    end=time.process_time()
    print(f"当前路径长:{alg.length}\t搜索时间:{end-start}s")
    DrawPath.drawPath(graph, alg.path,alg.lengths,alg.count)
    print("是否查看路径变化图？1.Yes 2.No")
    choose=int(input())
    if choose==1:
        DrawPath.showPath(graph,alg.paths)
    
