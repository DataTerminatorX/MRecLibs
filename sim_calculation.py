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
    1. 补全_cos_formula() 和 _pearson_formula() 用于评分类型
    2. 修改 get_sim_list() 函数，输入参数增加 sim_type 用于选择相似度类型
    3. 对于评分类型数据，考虑是否要将字典型数据转换成numpy的ndarray类型（参考之前给佳璐做的）
--------------
'''

import math,operator,copy
import itertools as it

class SimCalculation():

    def __init__(self,input_dict, K=float("inf"), sim_type = 'jaccard', form_type = 'init'):
        # input_dict: dictionary, <key: list(...)> 或者 <key: set(...)>, key:value 可以是 user:item，也可以是 item:user
        # sim_type: string, "jaccard"/"cos"/"pearson" 相似度(后两者待补充)
        # form_type: string, 对于jaccard距离: "init": 原始jaccard( |a ∩ b| / |a ∪ b| ) 
        #                                    "cos": 余弦jaccard( |a ∩ b|/ sqrt(|a|*|b|) )
        if not isinstance(sim_type, str):
            raise TypeError("'sim_type' must be str! %s found!"%(type(sim_type)))
        if not isinstance(form_type, str):
            raise TypeError("'form_type' must be str! %s found!"%(type(form_type)))
        if sim_type not in ("jaccard","cos","pearson"):
            raise ValueError("Value of 'sim_type' not support!")
        if form_type not in ("init","cos"):
            raise ValueError("Value of 'form_type' not support!")
        if not (isinstance(K, int) or K==float("inf")):
            raise TypeError("'K' must be int! %s found!"%(type(K)))
        if isinstance(input_dict, dict):
            self.input_dict = input_dict
            self.__sim_list = None
            self.__sim_dict = None
            self.sim_type = sim_type
            self.form_type = form_type
            self.K = K

            # intype: int, 0|1, 0: input_dict的value是list,(相似度计算不去重), 1: input_dict的value是set
            if isinstance(input_dict.values()[0], list):
                self.__intype = 0
            elif isinstance(input_dict.values()[0], set):
                self.__intype = 1
            else:
                raise TypeError("Value type of input_dict must be dict or set! %s found"%(type(input_dict.values()[0])))
        else:
            raise TypeError("Input type of SimCalculation must be dict! %s found!" %(type(input_dict)))

    def _jaccard_formula(self, a, b, form_type ):
        # 功能: 计算不同类型的jaccard相似度
        # 输入参数: 
            # a: list/set, 取决于intype的值
            # b: list/set, 取决于intype的值
            # form_type: str, "init": 原始jaccard( |a ∩ b| / |a ∪ b| ) 
            #                         "cos": 余弦jaccard( |a ∩ b|/ sqrt(|a|*|b|) )
        # 输出参数: 
            # jac_sim: int, a/b间的相似度

        if self.__intype == 0:

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
                # 可以看成两个value中相同元素、取出现次数少的，具体看印象笔记->团队会议->20160422
                num += min(a1[key], b1[key]) 
            if form_type == "init":
                den = len(a)+len(b)-num 
            else:
                den = math.sqrt(len(a)*len(b))

        else:
            num = len(a & b)
            if form_type == "init":
                den = len(a | b)
            else:
                den = math.sqrt(len(a)*len(b))
        return float(num)/den

    def _cos_formula(self): 
        # 代码待补充，入口参数个数与 _jaccard_formula 一致
        return

    def _pearson_formula(self):
        # 代码待补充，入口参数个数与 _jaccard_formula 一致
        return

    def get_sim_list (self):
        # 功能: 计算jaccard相似度
        # 输入参数:
            # input_dict: dictionary, <key: list(...)> 或者 <key: set(...)>, key:value 可以是 user:item，也可以是 item:user
        # 输出参数:
            # sim_list: list, 每个元素是(key1, key2, sim) (这里key是user或item), sim代表两者相似度

        if self.__sim_list is None:
            self.__sim_list = []
            sim_type_dict = {"jaccard":self._jaccard_formula, "cos": self._cos_formula, "pearson": self._pearson_formula}

            # 这段代码作废，用下面 combinations 高效实现
            # input_dict = copy.deepcopy(self.input_dict) # 先进行深拷贝, 因为下面会修改 input_dict
            # for key1, value1 in input_dict.items():
            #     for key2,value2 in input_dict.iteritems():
            #         if key1 == key2:          
            #             continue
            #         self.__sim_list.append( (key1, key2, sim_type_dict[self.sim_type](value2,value1,self.form_type) ) )
            #     input_dict.pop(key1) # 从input_dict中去掉key1，以免后面重复计算其他key和key1的相似度

            for (key1,value1), (key2,value2) in it.combinations(self.input_dict.iteritems(), 2):
                self.__sim_list.append( (key1, key2, sim_type_dict[self.sim_type](value2,value1,self.form_type) ) )

        return copy.deepcopy(self.__sim_list)
        # return self.__sim_list

    # def get_sim_dict ( sim_list, K ):
    def get_sim_dict ( self):
        # 功能: 处理上面得到的相似度list, 计算出最相似topK字典
        # 输入参数: 
            # sim_list: list, 每个元素是(key1, key2, sim) (这里key是user或item), sim代表两者相似度
            # K: int, 指定每个元素保留topK个最相似元素, 如果希望保留所有元素, 可以令 K = float("inf")
            # 其他: 当未生成 sim_list 时需要这些参数, 否则忽略
        # 输出参数:
            # topk_dict: dictionary, 每个元素是< key_i, sublist >, 其中sublist是与key_i(userid或itemid)最相近的K个key及其相似度值, 形式是 [(key_i1, 相似度值)..., (key_iK,相似度值)]


        if self.__sim_dict is None:
            self.__sim_dict = {}
            if self.__sim_list is None:
                self.__sim_list = self.get_sim_list()
            for e in self.__sim_list:
                self.__sim_dict.setdefault(e[0],[])
                self.__sim_dict[e[0]].append((e[1],e[2]))
                self.__sim_dict.setdefault(e[1],[])
                self.__sim_dict[e[1]].append((e[0],e[2]))
            for e in self.__sim_dict.iteritems():
                e[1].sort(key = operator.itemgetter(1), reverse = True)
                self.__sim_dict[e[0]] = e[1][0:min(len(e[1]), self.K)]

        return copy.deepcopy(self.__sim_dict)
        # return self.__sim_dict
            
            










