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
import cv2

if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    dest_dir = os.path.join(cur_dir, 'Merged_Cameras')
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)

    image_dirs = glob.glob('%s/Camera*' % cur_dir)
    print('Images dirs: ')
    for dir in image_dirs:
        print(dir)
    id = 0
    print('Merging images ... ')
    image_extensions = ['.jpg', '.png', '.JPG']
    for image_dir in image_dirs:
        images_list = os.listdir(image_dir)
        for image in images_list:
            if not any(image.endswith(ext) for ext in image_extensions):
                continue
            image_path = os.path.join(image_dir, image)
            if image.endswith('.jpg'):
                shutil.copy2(image_path, os.path.join(dest_dir, '%08d.jpg' % id))
            else:
                oriimage = cv2.imread(image_path)
                cv2.imwrite(os.path.join(dest_dir, '%08d.jpg' % id), oriimage)
            # shutil.copy2(image_path, os.path.join(dest_dir, '%08d.jpg' % id))
            id += 1
    print('Merging done ...')







