#!/usr/bin/env python
"""
Fetch the annotations, masks, and images for specific classes, and reindex them

Author: Tao Chen
Email: chentao904@163.com
Date: 2017.05.18
"""

from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import shutil
import os
import re
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

if __name__ == "__main__":
    class_wanted = ['floor']
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.join(cur_dir, 'Merged Labels')
    anno_path = os.path.join(root_dir, 'Annotations')
    image_path = os.path.join(root_dir, 'Images')
    mask_path = os.path.join(root_dir, 'Masks')

    dest_dir = os.path.join(cur_dir, 'Classes')
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    class_dir = {}
    for class_n in class_wanted:
        class_dir[class_n] = os.path.join(dest_dir, class_n)
        os.makedirs(class_dir[class_n])
        os.makedirs(os.path.join(class_dir[class_n], 'Annotations'))
        os.makedirs(os.path.join(class_dir[class_n], 'Images'))
        os.makedirs(os.path.join(class_dir[class_n], 'Masks'))
    images_list = os.listdir(image_path)
    print('Fetch classes: ', class_wanted)
    id_class = {cla: 0 for cla in class_wanted}
    for image in images_list:
        im_copy = {cla: False for cla in class_wanted}
        image_idx = image.split('.')[0]
        anno_file = os.path.join(anno_path, '%s.xml' % image_idx)
        if not os.path.exists(anno_file):
            continue
        tree = ET.ElementTree(file=anno_file)
        root = tree.getroot()

        for object in tree.iter('object'):
            class_name = object.find('name').text
            if class_name in class_wanted:
                im_copy[class_name] = True
                seg = object.find('segm')
                mask = seg.find('mask')
                mask_file = mask.text
                mask_file_path = os.path.join(mask_path, mask_file)
                new_mask = re.sub('\d\d\d\d\d\d\d\d', '%08d' % id_class[class_name], mask_file)
                shutil.copy2(mask_file_path, os.path.join(class_dir[class_name], 'Masks', new_mask))


        for class_n, flag in im_copy.iteritems():
            if flag:
                tree = ET.ElementTree(file=anno_file)
                root = tree.getroot()
                filename = tree.find('filename')
                filename.text = '%08d.jpg' % id_class[class_n]
                object_delete = []
                for object in tree.iter('object'):
                    class_name = object.find('name').text
                    if class_name != class_n:
                        object_delete.append(object)
                    else:
                        seg = object.find('segm')
                        mask = seg.find('mask')
                        mask_file = mask.text
                        mask.text = re.sub('\d\d\d\d\d\d\d\d', '%08d' % id_class[class_n], mask_file)
                        scribble = seg.find('scribbles')
                        scribble_name = scribble.find('scribble_name')
                        scribble_name_ori = scribble_name.text
                        scribble_name.text = re.sub('\d\d\d\d\d\d\d\d', '%08d' % id_class[class_n], scribble_name_ori)
                for object in object_delete:
                    root.remove(object)
                tree.write('%s/%08d.xml' % (os.path.join(class_dir[class_n], 'Annotations'), id_class[class_n]))
                shutil.copy2(os.path.join(image_path, image), os.path.join(class_dir[class_n],
                                                                           'Images', '%08d.jpg' % id_class[class_n]))
                id_class[class_n] += 1
    print('Fetching done ...')

