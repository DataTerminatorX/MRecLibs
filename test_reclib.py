#=== test "sim_calculation.py" module ====
import sim_calculation as simc

d = {1:[1,2,2,3,3], 2:[1,1,4], 3: [1,3,4,6,6], 4:[5]}
d1 = {key: set(value) for key,value in d.iteritems()}
# print  simc.get_sim_list(d, 0, "jaccard", "init")
# print  simc.get_sim_list(d, 0, "jaccard", "init")

sim_list = simc.get_sim_list(d1, 1, "jaccard", "init")
sim_dict = simc.get_sim_dict(sim_list , float("inf") )
# print sim_dict


#=== test "cf_models.py" module ====
import cf_models as cf
rec_dict,_,_ = cf.cf_full(d,0, "jaccard", "init", float("inf") , float("inf"))
print rec_dict
# K=float("inf")
# N=float("inf")
# sim_list = simc.get_sim_list(d, 0, "jaccard", "init")
# sim_dict = simc.get_sim_dict(sim_list , float("inf"))

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