#!/usr/bin/env python
"""
Delete annotations, masks, and images corresponding to user-specified images,
and redinexing these files

Author: Tao Chen
Email: chentao904@163.com
Date: 2017.05.19
"""

from __future__ import print_function
import shutil
import os
import glob
import re
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.join(cur_dir, 'Classes', 'floor')
    anno_path = os.path.join(root_dir, 'Annotations')
    image_path = os.path.join(root_dir, 'Images')
    mask_path = os.path.join(root_dir, 'Masks')
    dest_dir = os.path.join(root_dir, 'Cleaned')
    anno_dest_path = os.path.join(dest_dir, 'Annotations')
    image_dest_path = os.path.join(dest_dir, 'Images')
    mask_dest_path = os.path.join(dest_dir, 'Masks')
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)
    os.makedirs(anno_dest_path)
    os.makedirs(image_dest_path)
    os.makedirs(mask_dest_path)
    input = raw_input('Enter the specific image numbers whose labels you wanna delete (separated by commas):')
    input_list = input.split(',')
    raw_numbers = [x.strip() for x in input_list]
    for number in raw_numbers:
        try:
            number = int(number)
            print('Deleting labels corresponding to image %d' % number)
            image_file = os.path.join(image_path, '%08d.jpg' % number)
            anno_file = os.path.join(anno_path, '%08d.xml' % number)
            mask_files = glob.glob("%s/%08d_mask*.png" % (mask_path, number))
            files_to_delete = mask_files
            files_to_delete.append(anno_file)
            files_to_delete.append(image_file)
            for fileD in files_to_delete:
                if os.path.exists(fileD):
                    print('Deleting file %s' % fileD)
                    os.remove(fileD)
        except:
            print('%s is not an integer, ignoring it...' % number)
    print('Deleting labels done ... ')
    print('Reindexing files ...')
    id = 0
    images_list = os.listdir(image_path)
    for image in images_list:
        image_idx = image.split('.')[0]
        anno_file = os.path.join(anno_path, '%s.xml' % image_idx)
        if not os.path.exists(anno_file):
            continue
        mask_files = glob.glob("%s/%s_mask*.png" % (mask_path, image_idx))

        tree = ET.ElementTree(file=anno_file)
        root = tree.getroot()
        filename = tree.find('filename')
        filename.text = '%08d.jpg' % id
        delete_objects = []
        for object in tree.iter('object'):
            deleted = object.find('deleted')
            if int(deleted.text) == 1:
                delete_objects.append(object)
                continue
            seg = object.find('segm')
            if seg is None:
                continue

            mask = seg.find('mask')
            mask_text_ori = mask.text
            mask.text = re.sub('\d\d\d\d\d\d\d\d', '%08d' % id, mask_text_ori)
            scribble = seg.find('scribbles')
            scribble_name = scribble.find('scribble_name')
            scribble_name_ori = scribble_name.text
            scribble_name.text = re.sub('\d\d\d\d\d\d\d\d', '%08d' % id, scribble_name_ori)
        for object in delete_objects:
            root.remove(object)
        tree.write('%s/%08d.xml' % (anno_dest_path, id))
        shutil.copy2(os.path.join(image_path, image), os.path.join(image_dest_path, '%08d.jpg' % id))
        for mask in mask_files:
            mask_name = mask.split('/')[-1]
            new_mask = re.sub('\d\d\d\d\d\d\d\d', '%08d' % id, mask_name)
            shutil.copy2(mask, os.path.join(mask_dest_path, new_mask))
        id += 1
    print('Reindexing files done ...')