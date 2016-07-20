# ==== similarity calculation ======
'''
对于"有/无 交互" 类型的数据，计算jaccard相似度
若字典value为set，则调用经典的jaccard相似度
若字典value为list，调用不去重的jaccard相似度
--------------
后需改进的点：
1. 增加相似度种类(cos,pearson)
2. 对于评分类型的数据，改变计算公式
具体的：
    1. 补全cos_formula() 和 pearson_formula() 用于评分类型
    2. 修改 get_sim_list() 函数，输入参数增加 sim_type 用于选择相似度类型
    3. 对于评分类型数据，考虑是否要将字典型数据转换成numpy的ndarray类型（参考之前给佳璐做的）
--------------
'''

import math,operator,copy

def jaccard_formula( a, b, intype, form_type ):
    # 功能: 计算不同类型的jaccard相似度
    # 输入参数: 
        # a: list/set, 取决于intype的值
        # b: list/set, 取决于intype的值
        # intype: int, 0|1, 0: uidict的value是list,(相似度计算不去重), 1: uidict的value是set
        # form_type: str, "init": 原始jaccard( |a ∩ b| / |a ∪ b| ) 
        #                         "cos": 余弦jaccard( |a ∩ b|/ sqrt(|a|*|b|) )
    # 输出参数: 
        # jac_sim: int, a/b间的相似度

    if intype == 0:

        # 统计value中每个元素的出现次数，存在字典a1 b1里
        a1 = {}
        for key in a:
            a1.setdefault(key,0)
            a1[key] += 1
        b1 = {}
        for key in b:
            b1.setdefault(key,0)
            b1[key] += 1

        # 计算分子分母
        join_keys = set(a) & set(b)
        num = 0
        for key in join_keys:
            num += min(a1[key], b1[key]) # 可以看成两个value中相同元素、取出现次数少的，具体看印象笔记->团队会议->20160422
        if form_type == "init":
            den = len(a)+len(b)-num # 
        else:
            den = math.sqrt(len(a)*len(b))

    else:
        num = len(a & b)
        if form_type == "init":
            den = len(a | b)
        else:
            den = math.sqrt(len(a)*len(b))
    return float(num)/den

def cos_formula(): 
    # 代码待补充，入口参数个数与 jaccard_formula 一致
    return

def pearson_formula():
    # 代码待补充，入口参数个数与 jaccard_formula 一致
    return

def get_sim_list (uidict, intype, sim_type, form_type):
    # 功能: 计算jaccard相似度
    # 输入参数:
        # uidict: dictionary, <key: list(...)> 或者 <key: set(...)>, 取决于 intype 的取值. key:value 可以是 user:item，也可以是 item:user
        # intype: int, 0|1, 0: uidict的value是list, 1: uidict的value是set
        # sim_type: string, "jaccard"/"cos"/"pearson" 相似度(后两者待补充)
        # form_type: string, 对于jaccard距离: "init": 原始jaccard( |a ∩ b| / |a ∪ b| ) 
        #                                                       "cos": 余弦jaccard( |a ∩ b|/ sqrt(|a|*|b|) )
    # 输出参数:
        # sim_list: list, 每个元素是(key1, key2, sim) (这里key是user或item), sim代表两者相似度

    uidict = copy.deepcopy(uidict) # 先进行深拷贝, 因为下面会修改 uidict
    sim_type_dict = {"jaccard":jaccard_formula, "cos": cos_formula, "pearson": pearson_formula}
    sim_list = []
    for key1, value1 in uidict.items():
        for key2,value2 in uidict.iteritems():
            if key1 == key2:          
                continue
            sim_list.append( (key1, key2, sim_type_dict[sim_type](value2,value1,intype, form_type) ) )
        uidict.pop(key1) # 从uidict中去掉key1，以免后面重复计算其他key和key1的相似度
    return sim_list

def get_sim_dict ( sim_list, K ):
    # 功能: 处理上面得到的相似度list, 计算出最相似topK字典
    # 输入参数: 
        # sim_list: list, 每个元素是(key1, key2, sim) (这里key是user或item), sim代表两者相似度
        # K: int, 指定每个元素保留topK个最相似元素, 如果希望保留所有, 可以令 K = float("inf")
    # 输出参数:
        # topk_dict: dictionary, 每个元素是< key_i, sublist >, 其中sublist是与key_i(userid或itemid)最相近的K个key及其相似度值, 形式是 [(key_i1, 相似度值)..., (key_iK,相似度值)]

    sim_dict = {}
    for e in sim_list:
        sim_dict.setdefault(e[0],[])
        sim_dict[e[0]].append((e[1],e[2]))
        sim_dict.setdefault(e[1],[])
        sim_dict[e[1]].append((e[0],e[2]))
    for e in sim_dict.iteritems():
        e[1].sort(key = operator.itemgetter(1), reverse = True)
        sim_dict[e[0]] = e[1][0:min(len(e[1]), K)]
    return sim_dict
        
        










