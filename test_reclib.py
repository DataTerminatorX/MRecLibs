#=== test "sim_calculation.py" module ====

from sim_calculation import SimCalculation as SimC
from models import CF
from ConfigParser import SafeConfigParser
import logging


d = {'a':[1,2,2,3,3], 2:[1,1,4], 3: [1,3,4,6], 4:[5]}
d1 = {key: set(value) for key,value in d.iteritems()}
# print  simc.get_sim_list(d, 0, "jaccard", "init")
# print  simc.get_sim_list(d, 0, "jaccard", "init")

# simc = SimC(d1)
# s1 = simc.get_sim_list()
# s2 = simc.get_sim_dict()
# print s1
# print s2


# ==convert sim_list to ndarray X with shape(n_samples, n_samples)==

# import numpy as np
# import scipy as sp
# keys = sim_dict.keys()
# X = np.zeros((len(keys),len(keys)) )
# for e in sim_list:
    # if e[2] <> 0:
        # i = keys.index(e[0])
        # j = keys.index(e[1])
        # X[i,j]= e[2]
        # X[j,i]= e[2]
# sX = sp.csr_matrix(X) # convert to row sparse matrix if needed


#=== test "cf_models.py" module ====

# import cf_models as cf
# rec_dict,_,_ = cf.cf_full(d,0, "jaccard", "init", float("inf") , float("inf"))
# print rec_dict

# K=float("inf")
# N=float("inf")
# sim_list = simc.get_sim_list(d, 0, "jaccard", "init")
# sim_dict = simc.get_sim_dict(sim_list , float("inf"))

ucf = CF('user', d1)
ucf.train_predict()
print ucf.get_rec_filter()


# rec_dict={}
# for key, l in sim_dict.iteritems(): 
    # print key, l
    # rec_dict.setdefault(key)
    # d = {}
    # sum_sim=0
    # for key_neighbor, sim in l:
        # sum_sim += sim
        
        # print sum_sim
        # iset = set(input_dict[key_neighbor]) # 当输入的uidict为list时, 已经在计算相似度矩阵时考虑了重复情形, 在做推荐时应消重
        # for ikey in iset:
            # d.setdefault(ikey,0)
            # d[key2] += sim
           
    # d =  {key:value/(0.01 if sum_sim==0 else sum_sim) for key,value in d.iteritems()}# 计算总的sim值f
    # rec_dict[key] = sorted(d.iteritems(), key = operator.itemgetter(1),reverse = True)[0:min(len(d[key]),N)]
    
    # print rec_dict[key]