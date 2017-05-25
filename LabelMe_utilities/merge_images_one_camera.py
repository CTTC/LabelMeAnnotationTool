#!/usr/bin/env python
"""
Merge folders Camera*, ...
And reindex image_ids

Author: Tao Chen
Email: chentao904@163.com
Date: 2017.05.22
"""

from __future__ import print_function
import shutil
import os
import glob

if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    dest_dir = os.path.join(cur_dir, 'Merged_Cameras')
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    image_dirs = glob.glob('%s/Camera*' % cur_dir)
    print('Images dir: ', image_dirs)
    id = 0
    print('Merging images ... ')
    for image_dir in image_dirs:
        images_list = os.listdir(image_dir)
        for image in images_list:
            image_path = os.path.join(image_dir, image)
            shutil.copy2(image_path, os.path.join(dest_dir, '%08d.jpg' % id))
            id += 1
    print('Merging done ...')







