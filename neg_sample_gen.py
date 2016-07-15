# ======== negative samples generation =====
'''
生成负样本，适用于没有显示负样本的推荐问题
Step1. 从交互item数较多的user中抽样user
Step2. 从被user交互较多的item中抽样item
Step3. 两者结合, 得到未被user交互的item, 负样本
后续改进的点: 1. 综合交互数、item价格、item评分等来抽样user/item 2. 带权抽样 3. 输入参数异常处理
'''

import random as rd
import operator

def user_sampling( u_i_dict, th, sample_rate ):
	# 功能：抽样行为特征强的user
	# 输入参数:
	# u_i_dict: dictionary, <user-id, list[ item-id ]> 或者 <user-id, set(item-id)>，按需使用，list包含重复购买的商品，set不包含
	# th: float or int, (0,1], 对user-id排序后选取前th的user作为待采样的user
	# sample_rate: float or int, (0,1], 定义采样比例
	# 输出参数:
	# set(u_list): set, user的集合

	u_i_dict = {uid:len(u_i_dict[uid]) for uid in u_i_dict}
	u_list = sorted(u_i_dict.iteritems(), key=operator.itemgetter(1), reverse=True)  # 按user行为数来
	n = len(u_list)
	ns = int(n*th)
	u_list = [ u_list[idx][0] for idx in rd.sample( xrange(ns), int(ns*sample_rate) ) ]

	return set(u_list)

def item_sampling( i_u_dict, th, sample_rate ):
	# 功能: 抽样行为特征强的item
	# 输入参数:
	# i_u_dict: dictionary, <item-id, list[ user-id ]> 或者 <item-id, set(user-id)>，按需使用，list包含重复购买的商品，set不包含
	# th: float or int, (0,1], 对item-id排序后选取前th的item作为待采样的item
	# sample_rate: float or int, (0,1], 定义采样比例
	# 输出参数:
	# set(i_list): set, item的集合

	i_u_dict = {iid:len(i_u_dict[iid]) for iid in i_u_dict}
	i_list = sorted(i_u_dict.iteritems(), key=operator.itemgetter(1), reverse=True)  # 按user行为数来
	n = len(i_list)
	ns = int(n*th)
	i_list = [ i_list[idx][0] for idx in rd.sample( xrange(ns), int(ns*sample_rate )) ]

	return set(i_list)

def neg_sample_generation( pos_dict, u_i_dict, i_u_dict, intype, th, sample_rate_u, sample_rate_i):
	# 功能：生成负样本字典集
	# 输入参数:
	# pos_dict: dictionary, 所有正样本, 即有交互的<user-id, set(item-id)> 或者 <item-id, set(user-id)>, 取决于"intype"参数
	# intype: int, 0|1，0: 输入输出的pos_dict是user-id为key，1：是item-id为key. intype的default是0
	# u_i_dict, i_u_dict,th,sample_rate_u, sample_rate_i: 见 user_sampling(...) 和 item_sampling(...) 的参数介绍
	# 输出参数:
	# neg_dict: dictionary, <user-id, set(item-id)> 或者 <item-id, set(user-id)>, 跟pos_dict的pair一致
	
	if intype == 1:
		value_set = user_sampling( u_i_dict, th, sample_rate_u)
		key_set = item_sampling( i_u_dict, th, sample_rate_i)
	else:
		value_set = item_sampling( i_u_dict, th, sample_rate_i)
		key_set = user_sampling( u_i_dict, th, sample_rate_u)
	neg_dict = { key:value_set-pos_dict[key] for key in key_set if len(value_set-pos_dict[key])>0 }

	return neg_dict
