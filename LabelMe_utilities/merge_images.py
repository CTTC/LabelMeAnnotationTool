#!/usr/bin/env python
"""
Merge folders Images, Images, Images, Images, ...
And reindexing image_ids

Author: Tao Chen
Email: chentao904@163.com
Date: 2017.05.16
"""


import shutil
import os
import glob

if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    dest_dir = os.path.join(cur_dir, 'Merged_Images')
    left_dest_path = os.path.join(dest_dir, 'Left')
    right_dest_path = os.path.join(dest_dir, 'Right')
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)
    os.makedirs(left_dest_path)
    os.makedirs(right_dest_path)

    image_dirs = glob.glob('%s/Images*' % cur_dir)
    print('Images dir: ', image_dirs)
    id = 0
    print('Merging images ... ')
    for image_dir in image_dirs:
        left_path = os.path.join(image_dir, 'Left')
        right_path = os.path.join(image_dir, 'Right')
        if not os.path.exists(left_path):
            continue
        images_list = os.listdir(left_path)
        for left_image in images_list:
            right_image = left_image.replace('L', 'R')
            left_image_path = os.path.join(left_path, left_image)
            right_image_path = os.path.join(right_path, right_image)

            shutil.copy2(left_image_path, os.path.join(left_dest_path, 'L%08d.jpg' % id))
            shutil.copy2(right_image_path, os.path.join(right_dest_path, 'R%08d.jpg' % id))
            id += 1
    print('Merging done ...')







