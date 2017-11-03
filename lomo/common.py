import random

# 生成随机数

def generate_choice(count):
	num_list = []
	# 从1～100之间生成n个随机数
	for i in range(0,count-1):
		choice = random.choice(range(1,100))
		if choice not in num_list:
			num_list.append(choice)
	# 从小到大排序随机数列表
	num_list.sort()
	# 根据随机数列表的到差值列表
	i = 0
	result_list = []

	list_count = len(num_list) + 1

	for index in range(0,list_count):
		if index != len(num_list):
			result_list.append(num_list[index]- i)
			i = num_list[index]
		else:
			result_list.append(100 - i)

	return result_list

