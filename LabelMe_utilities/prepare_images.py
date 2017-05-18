#!/usr/bin/env python
"""
Merge left and right images into one folder and 
separating them into several evenly sized chunks

Author: Tao Chen
Email: chentao904@163.com
Date: 2017.05.16
"""

from __future__ import print_function
import shutil
import os
import re
import errno
import numpy as np

if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    save_path = os.path.join(cur_dir, 'Merged_Images')
    left_path = os.path.join(save_path, 'Left')
    right_path = os.path.join(save_path, 'Right')
    left_image_list = os.listdir(left_path)
    right_image_list = os.listdir(right_path)
    dest_path = os.path.join(cur_dir, 'Merged_LR')
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    else:
        print('Folder to store merged images already exist, do you want to delete it? ( \'y\' or \'n\')')
        while True:
            keyboard_input = raw_input("Enter your choice:\n")
            if keyboard_input == 'y':
                shutil.rmtree(dest_path)
                os.makedirs(dest_path)
                break
            elif keyboard_input == 'n':
                break
            else:
                print("Unrecognized response, please enter \'y\' or \'n\'")

    same_image_num = min(len(left_image_list), len(right_image_list))

    files_lst = os.listdir(dest_path)
    max_index = 0
    for filename in files_lst:
        fileindex_list = re.findall(r'\d+', filename)
        if not fileindex_list:
            continue
        fileindex = int(fileindex_list[0])
        if fileindex >= max_index:
            max_index = fileindex
    count = max_index + 1 if max_index > 0 else max_index

    print('Start merging images ...')
    for idx in xrange(same_image_num):
        left_image = os.path.join(left_path, 'L%08d.jpg' % idx)
        right_image = os.path.join(right_path, 'R%08d.jpg' % idx)
        new_image = os.path.join(dest_path, '%08d.jpg' % count)
        shutil.copy2(left_image, new_image)
        count += 1
        new_image = os.path.join(dest_path, '%08d.jpg' % count)
        shutil.copy2(right_image, new_image)
        count += 1

    if same_image_num < len(left_image_list):
        for idx in xrange(same_image_num, len(left_image_list)):
            image = os.path.join(left_path, 'L%08d.jpg' % idx)
            new_image = os.path.join(dest_path, '%08d.jpg' % count)
            shutil.copy2(image, new_image)
            count += 1
    elif same_image_num < len(right_image_list):
        for idx in xrange(same_image_num, len(right_image_list)):
            image = os.path.join(right_path, 'L%08d.jpg' % idx)
            new_image = os.path.join(dest_path, '%08d.jpg' % count)
            shutil.copy2(image, new_image)
            count += 1

    print('Merging images done ...')
    print('Start separating images ...')
    merged_path = dest_path
    merged_files = os.listdir(merged_path)
    num_sep = 4
    tgt_folders = []
    for idx in xrange(num_sep):
        folder = os.path.join(cur_dir, '%d'%idx)
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            shutil.rmtree(folder)
            os.makedirs(folder)
        tgt_folders.append(folder)
    num_files = len(merged_files)
    sep_chunk = np.array_split(range(num_files), num_sep)
    for index, chunk in enumerate(sep_chunk):
        chunk = chunk.tolist()
        for idx in chunk:
            folder = tgt_folders[index]
            src = os.path.join(merged_path, '%08d.jpg' % idx)
            dst = os.path.join(folder)
            shutil.copy2(src, dst)
    print('Separating images done ...')







