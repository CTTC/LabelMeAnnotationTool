#!/usr/bin/env python
"""
Resize images

Author: Tao Chen
Email: chentao904@163.com
Date: 2017.05.25
"""

from __future__ import print_function
import cv2
import os
import shutil

if __name__ == "__main__":
    print('Resize images  ...')

    cur_dir = os.path.dirname(os.path.realpath(__file__))
    src_dir = os.path.join(cur_dir, 'Merged_Cameras')
    dest_dir = os.path.join(cur_dir, 'Resized_Cameras')
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)
    newx = 640
    newy = 480
    images = os.listdir(src_dir)
    for image in images:
        image_idx = image.split('.')[0]
        image_path = os.path.join(src_dir, image)
        oriimage = cv2.imread(image_path)
        resized = cv2.resize(oriimage, (newx, newy), interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join(dest_dir, '%s.jpg' % image_idx), resized)
    print('Resizing done ...')