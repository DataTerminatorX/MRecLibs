
# ==== collaborative filtering models ======
'''
计算相似度，得到每个user/item的topK相似度字典，预测用户购买行为
ToDo: 接受额外的用户相似度矩阵和uidict(即不是通过uidict产生的相似度矩阵) ，然后做推荐。
'''

from sim_calculation import SimCalculation as SimC
import operator, logging

class CF():
    def __init__(self, model_type,  input_dict,K=float("inf"), sim_dict = None,sim_type = 'jaccard', form_type = 'init'):
        # 输入:
            # model_type: 'item' 或 'user', 分别代表 itemCF 和 userCF 
            # input_dict: 输入是 uidict或iudict, 且 <key: set(...)> 或  <key: list(...)>, key 是user 或 item
            # N: int, 最后推荐结果中截取前N个, 需要全部结果可设置为 float("inf")
            # sim_dict: 如果给出, 就不用计算 sim_dict
            # sim_type: string, "jaccard"/"cos"/"pearson" (详见 sim_calculation.py->get_sim_list() )
            # form_type: string, 对于jaccard距离: "init": 原始jaccard( |a ∩ b| / |a ∪ b| )                                                       
            #                                   "cos": 余弦jaccard( |a ∩ b|/ sqrt(|a|*|b|) )  
        if not isinstance(model_type, str):
            raise TypeError("'model_type' must be str! %s found!"%(type(model_type)))
        if model_type not in ("item","user"):
            raise ValueError("Value of 'model_type' not support!")
        if not isinstance(sim_type, str):
            raise TypeError("'sim_type' must be str! %s found!"%(type(sim_type)))
        if sim_type not in ("jaccard","cos","pearson"):
            raise ValueError("Value of 'sim_type' not support!")
        if not isinstance(form_type, str):
            raise TypeError("'form_type' must be str! %s found!"%(type(form_type)))
        if form_type not in ("init","cos"):
            raise ValueError("Value of 'form_type' not support!")
        if not (isinstance(K, int) or K==float("inf")):
            raise TypeError("'K' must be int! %s found!"%(type(K)))
        if not isinstance(input_dict, dict):
            raise TypeError("'input_dict' must be dict! %s found!" %(type(input_dict)))                  
        
        self.model_type = model_type
        self.input_dict = input_dict
        # K: int, 选取 K 个邻居用于推荐, 需要全部邻居可设置为 float("inf") 
        self.K = K
        self.__sim_dict = sim_dict
        self.rec_dict = None
        self.sim_type = sim_type
        self.form_type = form_type

    def train_predict(self):
        # 功能: 实现 user based CF 和 item based CF, 根据topK 个相似邻居计算相似度 (注意, 如果输入是 item-user 字典, 则输出结果是 <item: list(topN users)>, 需要自行处理成 <user: list(items)>)
        # 输出: 
            # rec_dict: dictionary,  <key: list(topK elements)>, 其中list的元素为: (key: similarity_score)
            # sim_list: list, (key1, key2, sim)
            # sim_dict: dictionary, <key: list>, 详见 sim_calculation.py->get_sim_dict()
        
        # print ">>>> generating similarity matrix <<<<"
        # logging.info(">>>> generating similarity matrix <<<<")
        # sim_list = SimC(input_dict).get_sim_list(sim_type, form_type)
        
        # print ">>>> generating topK similar neighbours <<<<"
        if self.__sim_dict is None:
            logging.info(">>>> generating topK similar neighbours <<<<")
            self.__sim_dict = SimC(self.input_dict, self.K, self.sim_type, self.form_type).get_sim_dict()
        if not isinstance(self.__sim_dict, dict):
            raise TypeError("Input type of SimCalculation must be dict! %s found!" %(type(self.__sim_dict)))        


        # 以下根据公式 score(ui,vj) = Σ sim(ui, uk)*1(uk,vj) /Σ sim(ui, uk), uk ∈ {ui的topK 邻居}
        if self.rec_dict is None:
            self.rec_dict={}
            idx = 0
            for key, l in self.__sim_dict.iteritems(): 
                idx += 1
                if idx%100==0:
                    # print ">>>> processing the "+str(idx)+"th user/item recommendation <<<<"
                    logging.info(">>>> processing the "+str(idx)+"th user/item recommendation <<<<")
                self.rec_dict.setdefault(key)

                # d: 以 user-item 为例, d.key = 该user的topK相似users购买的items, d.value=对item的打分
                # 注意: 对于没有出现在这topK个user里的item，d里也不会出现
                d = {}
                sum_sim=0
                for key_neighbor, sim in l:
                    sum_sim += sim
                    iset = set(self.input_dict[key_neighbor]) # 当输入的input_dict为list时, 已经在计算相似度矩阵时考虑了重复情形, 在做推荐时应去重
                    for ikey in iset:
                        d.setdefault(ikey,0)
                        d[ikey] += sim
                       
                d =  {k:v/(0.01 if sum_sim==0 else sum_sim) for k,v in d.iteritems()}# 计算总的sim值f

                # Todo: 输入 全体 key 的集合，用0填充 d 中未出现的 key 生成rec_dict

                self.rec_dict[key] = sorted(d.iteritems(), key = operator.itemgetter(1),reverse = True)
            
            if self.model_type=='item':
                pass


    def get_rec(self, N=float('inf')):
        # 截取结果的前N个
        if not (isinstance(N, int) or N==float("inf")):
            raise TypeError("'N' must be int! %s found!"%(type(N)))
 
        return {key:value[0:min(len(value),N)] for key,value in self.rec_dict.iteritems()}

    def get_rec_filter(self):
        # 功能: 在 cf_full 的结果上，分别获取 (推荐集合 U 原有集合) 和 (推荐集合 - 原有集合)
        tmp = {}
        for key,value in self.rec_dict.iteritems():
            buylist = self.input_dict[key]
            value = [(e1,e2) for e1,e2 in value if e1 not in buylist]
            tmp.setdefault(key, value)
        return tmp

    # ==== matrix factorization models =====