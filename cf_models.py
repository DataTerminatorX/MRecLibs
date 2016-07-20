
# ==== collaborative filtering models ======
'''
计算相似度，得到每个user/item的topK相似度字典，预测用户购买行为
ToDo: 接受额外的用户相似度矩阵和uidict(即不是通过uidict产生的相似度矩阵) ，然后做推荐。
'''

import sim_calculation as simc
import operator

def cf_full(input_dict, dict_type, sim_type, form_type,  K, N):
    # 功能: 实现 user based CF 和 item based CF, 根据topK 个相似邻居计算相似度, 截取结果的前N个 (注意, 如果输入是 item-user 字典, 则输出结果是 <item: list(topN users)>, 需要自行处理成 <user: list(items)>)
    # 输入: 
        # input_dict: 
        #               若 dict_type = 0, 则输入是 uidict或iudict, 且 <key: list(...)>, key 是user 或 item
        #               若 dict_type = 1, 则输入是 uidict或iudict, 且 <key: set(...)>
        # dict_type: 0|1 , 对应上面不同input_dict 类型
        # sim_type: string, "jaccard"/"cos"/"pearson" (详见 sim_calculation.py->get_sim_list() )
        # form_type: string, 对于jaccard距离: "init": 原始jaccard( |a ∩ b| / |a ∪ b| )  
        #                                                       "cos": 余弦jaccard( |a ∩ b|/ sqrt(|a|*|b|) )
        # K: int, 选取 K 个邻居用于推荐, 需要全部邻居可设置为 float("inf") 
        # N: int, 最后推荐结果中截取前N个, 需要全部结果可设置为 float("inf")
    # 输出: 
        # rec_dict: dictionary,  <key: list(topK elements)>, 其中list的元素为: (key: similarity_score)
        # sim_list: list, (key1, key2, sim)
        # sim_dict: dictionary, <key: list>, 详见 sim_calculation.py->get_sim_dict()
    sim_list = simc.get_sim_list(input_dict, dict_type, sim_type, form_type)
    sim_dict = simc.get_sim_dict(sim_list , K )
    
    # 以下根据公式 score(ui,vj) = Σ sim(ui, uk)*1(uk,vj) /Σ sim(ui, uk), uk ∈ {ui的topK 邻居}
    rec_dict={}
    for key, l in sim_dict.iteritems(): 
        rec_dict.setdefault(key)
        d = {}
        sum_sim=0
        for key_neighbor, sim in l:
            sum_sim += sim
            iset = set(input_dict[key_neighbor]) # 当输入的uidict为list时, 已经在计算相似度矩阵时考虑了重复情形, 在做推荐时应消重
            for ikey in iset:
                d.setdefault(ikey,0)
                d[ikey] += sim
               
        d =  {k:v/(0.01 if sum_sim==0 else sum_sim) for k,v in d.iteritems()}# 计算总的sim值f
        rec_dict[key] = sorted(d.iteritems(), key = operator.itemgetter(1),reverse = True)[0:min(len(d.keys()),N)]
        
    return rec_dict, sim_list, sim_dict
    
def cf_filter():
    # 功能: 在 cf_full 的结果上，分别获取 (推荐集合 U 原有集合) 和 (推荐集合 - 原有集合)
    # 
#    rec_dict =
    return

# ==== matrix factorization models =====