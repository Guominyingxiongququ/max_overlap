import pdb
import numpy as np
import operator
import cv2
import os
from PIL import Image

def _get_voc_color_map(n=256):
    color_map = np.zeros((n, 3))
    for i in xrange(n):
        r = b = g = 0
        cid = i
        for j in xrange(0, 8):
            r = np.bitwise_or(r, np.left_shift(np.unpackbits(np.array([cid], dtype=np.uint8))[-1], 7-j))
            g = np.bitwise_or(g, np.left_shift(np.unpackbits(np.array([cid], dtype=np.uint8))[-2], 7-j))
            b = np.bitwise_or(b, np.left_shift(np.unpackbits(np.array([cid], dtype=np.uint8))[-3], 7-j))
            cid = np.right_shift(cid, 3)

        color_map[i][0] = r
        color_map[i][1] = g
        color_map[i][2] = b
    return color_map

def replace_label(image,box,origin_label,target_label):
	for i in range(box[0],box[2]+1):
		for j in range(box[1], box[3]+1):
			if image[j][i] == origin_label:
				image[j][i] = target_label

def get_box_instance(matrix, box):
	label_num = [0] * 100
	for i in range(box[0],box[2]+1):
		for j in range(box[1], box[3]+1):
			cur_label = matrix[j][i]
			if cur_label<100:
				label_num[cur_label] = label_num[cur_label] + 1
	index, value = max(enumerate(label_num), key=operator.itemgetter(1))
	return index

def check_overlap(origin_box, target_box):
	overlap = -1
	minx = max(origin_box[0],target_box[0])
	miny = max(origin_box[1],target_box[1])
	maxx = min(origin_box[2],target_box[2])
	maxy = min(origin_box[3],target_box[3])

	if not(minx>maxx or miny> maxy):
		overlap = (maxx-minx)*(maxy-miny)
	return overlap

if __name__ == '__main__':
	max_frame_idx = 1100
	default_inst_idx = 1
	res_list=[]

	img_box_list = []
	for i in range(0,1100):
		img_box_list.append([])

	with open ("sorted_inst_box.txt",'r') as f:
		content = f.readlines()
		for x in content:
			x = x.strip()
			cur_file , box_0, box_1, box_2, box_3 = x.split(",")
			cur_file = cur_file.strip()
			box_0 = box_0.strip()
			box_1 = box_1.strip()
			box_2 = box_2.strip()
			box_3 = box_3.strip()
			res_dict = {'file_name': cur_file,
	                'box_0': int(box_0),
	                'box_1': int(box_1),
	                'box_2': int(box_2),
	                'box_3': int(box_3)}
			res_list.append(res_dict)
	for res_dict in res_list:
		cur_name = res_dict['file_name'][:-4]
		idx = int(cur_name)
		box = [res_dict['box_0'],res_dict['box_1'],res_dict['box_2'],res_dict['box_3'],-1]
		img_box_list[idx].append(box)

	# set instance label

	cur_label = 1

	# get start frame
	start_frame = 0
	for i in range(0,1100):
		if len(img_box_list[i])!=0:
			start_frame = i
			break

	for i in range(start_frame, 1100):
		for box in img_box_list[i]:
			if box[4]==-1:
				box[4] = cur_label
				cur_label = cur_label + 1
	#check the next frame
			if i!=1098:
				set_idx = -1
				overlap_size = -1
				cur_idx = 0
				for next_box in img_box_list[i+1]:
					cur_size = check_overlap(box, next_box)
					if cur_size>overlap_size:
						set_idx = cur_idx
						overlap_size = cur_size
					cur_idx = cur_idx + 1
				if set_idx!=-1:
					img_box_list[i+1][set_idx][4] = box[4]
	color_map = _get_voc_color_map()
	#set instance label
	img_height = 250
	img_width = 500
	for i in range(start_frame, 1100):
		print i
		cur_i = i
		img_file_name = "inst_" + str(i).zfill(6) +".pgm"
		image = np.loadtxt(img_file_name, dtype='i')
		for box in img_box_list[i]:
			origin_label = get_box_instance(image,box)
			target_label = box[4]
			replace_label(image,box,origin_label,target_label)
		target_colored_file = "../../output/inst_" + str(i).zfill(6) +".png"
		colored_out_img = np.zeros((img_height, img_width, 3))
		for k in xrange(img_height):
			for j in xrange(img_width):
				colored_out_img[k][j] = color_map[image[k][j]][::-1]
		cv2.imwrite(target_colored_file, colored_out_img)
		gt_image = str(i).zfill(6) +".jpg"
		background = Image.open(gt_image)
		mask = Image.open(target_colored_file)
		background = background.convert('RGBA')
		mask = mask.convert('RGBA')
		superimpose_image = Image.blend(background, mask, 0.6)
		superimpose_name = "../../output/inst_final_" + str(cur_i).zfill(6) +'.jpg'
		superimpose_image.save(superimpose_name, 'JPEG')
		im = cv2.imread(superimpose_name)
