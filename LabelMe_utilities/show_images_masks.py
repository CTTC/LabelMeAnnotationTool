#!/usr/bin/env python
"""
Show original images overlayed with masks

Author: Tao Chen
Email: chentao904@163.com
Date: 2017.05.18
"""

from __future__ import print_function
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.join(cur_dir, 'Augmented Images')
    # root_dir = os.path.join(cur_dir, 'Classes', 'floor')
    anno_path = os.path.join(root_dir, 'Annotations')
    image_path = os.path.join(root_dir, 'Images')
    mask_path = os.path.join(root_dir, 'Masks')

    num_images = os.listdir(image_path)
    check_list = range(50)#range(len(num_images))
    alpha = 0.4
    for idx in check_list:
        image_name = '%08d.jpg' % idx
        idx_im_path = os.path.join(image_path, image_name)
        if not os.path.exists(idx_im_path):
            print('Image %s does not exist, ignoring it ...' % image_name)
            continue
        image_base = cv2.imread(idx_im_path)
        image = image_base.copy()

        anno_name = '%08d.xml' % idx
        idx_anno_path = os.path.join(anno_path, anno_name)
        tree = ET.ElementTree(file=idx_anno_path)
        root = tree.getroot()
        mask_names = []
        classes = []
        text_poses = []
        for object in tree.iter('object'):
            seg = object.find('segm')
            deleted = object.find('deleted')
            if int(deleted.text) == 1 or seg is None:
                continue
            mask = seg.find('mask')
            pos = seg.find('box')
            x_min = int(pos.find('xmin').text)
            y_min = int(pos.find('ymin').text)
            x_max = int(pos.find('xmax').text)
            y_max = int(pos.find('ymax').text)
            y_min = 20 if y_min < 20 else y_min
            up_mid_pos = [(x_min + x_max) / 2.0, y_min]
            up_mid_pos = [int(i) for i in up_mid_pos]
            mask_names.append(mask.text)
            classes.append(object.find('name').text)
            text_poses.append(up_mid_pos)
        for mask in mask_names:
            idx_mask_path = os.path.join(mask_path, mask)
            mask_im = cv2.imread(idx_mask_path)
            gray_mask = cv2.cvtColor(mask_im, cv2.COLOR_BGR2GRAY)
            mask_row, mask_col = np.where(gray_mask > 1)
            image[mask_row, mask_col] = alpha * mask_im[mask_row, mask_col] + (1 - alpha) * image[mask_row, mask_col]

        for class_type, text_pos in zip(classes, text_poses):
            cv2.putText(image, '%s' % class_type, tuple(text_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        # cv2.imshow('Testing', image)
        # cv2.waitKey(0)
        plt.cla()
        plt.title('%s' % image_name)
        plt.axis("off")
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.show()





