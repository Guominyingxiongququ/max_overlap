if __name__ == '__main__':
	max_frame_idx = 1100
	default_inst_idx = 1
	res_list=[]
	output_file = 'sorted_inst_box.txt'
	with open ("inst_box.txt",'r') as f:
		content = f.readlines()
		for x in content:
			print x
			x = x.strip()
			cur_file , box_0, box_1, box_2, box_3 = x.split(",")
			res_dict = {'file_name': cur_file,
	                'box_0': box_0,
	                'box_1': box_1,
	                'box_2': box_2,
	                'box_3': box_3}
			res_list.append(res_dict)
	res_list = sorted(res_list,key=lambda i: i['file_name'])
	print merge(res_list, key=lambda x: x['file_name'])
	# f =open(output_file,"w")
	# for res in res_list:
	# 	print >> f, "%s,%s,%s,%s,%s" % (res['file_name'], res['box_0'], res['box_1'], res['box_2'], res['box_3'])
	# f.close()
