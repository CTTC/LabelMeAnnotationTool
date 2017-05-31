#!/usr/bin/env python
"""
Change the brightness, contrast of images, duplicate 
the corresponding labels 

Author: Tao Chen
Email: chentao904@163.com
Date: 2017.05.25
"""

from __future__ import print_function
import cv2
from PIL import Image, ImageEnhance
import os
import glob
import re
import shutil
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def save_anno_mask(anno_file, mask_files, anno_dest_path, mask_dest_path, id):
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

    for mask in mask_files:
        mask_name = mask.split('/')[-1]
        new_mask = re.sub('\d\d\d\d\d\d\d\d', '%08d' % id, mask_name)
        shutil.copy2(mask, os.path.join(mask_dest_path, new_mask))

if __name__ == "__main__":
    print('Changing the brightness and contrast of images  ...')

    cur_dir = os.path.dirname(os.path.realpath(__file__))
    root_dir = os.path.join(cur_dir, 'Merged Labels')
    # root_dir = os.path.join(cur_dir, 'Labels0')
    anno_src_path = os.path.join(root_dir, 'Annotations')
    image_src_path = os.path.join(root_dir, 'Images')
    mask_src_path = os.path.join(root_dir, 'Masks')
    dest_dir = os.path.join(cur_dir, 'Augmented Images')
    anno_dest_path = os.path.join(dest_dir, 'Annotations')
    image_dest_path = os.path.join(dest_dir, 'Images')
    mask_dest_path = os.path.join(dest_dir, 'Masks')
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)
    os.makedirs(anno_dest_path)
    os.makedirs(image_dest_path)
    os.makedirs(mask_dest_path)

    images = os.listdir(image_src_path)
    idx = 0
    for image in images:
        image_idx = image.split('.')[0]
        try:
            image_i = int(image_idx)
        except:
            continue
        image_path = os.path.join(image_src_path, image)
        anno_file = os.path.join(anno_src_path, '%s.xml' % image_idx)
        if not os.path.exists(anno_file):
            continue
        mask_files = glob.glob("%s/%s_mask*.png" % (mask_src_path, image_idx))

        shutil.copy2(image_path, os.path.join(image_dest_path, '%08d.jpg' % idx))
        save_anno_mask(anno_file, mask_files, anno_dest_path, mask_dest_path, idx)
        idx += 1

        oriimage = Image.open(image_path)
        enhancer = ImageEnhance.Contrast(oriimage)
        newimage = enhancer.enhance(1.2)
        newimage.save(os.path.join(image_dest_path, '%08d.jpg' % idx))
        save_anno_mask(anno_file, mask_files, anno_dest_path, mask_dest_path, idx)
        idx += 1

        newimage = enhancer.enhance(0.8)
        newimage.save(os.path.join(image_dest_path, '%08d.jpg' % idx))
        save_anno_mask(anno_file, mask_files, anno_dest_path, mask_dest_path, idx)
        idx += 1

        enhancer = ImageEnhance.Brightness(oriimage)
        newimage = enhancer.enhance(1.2)
        newimage.save(os.path.join(image_dest_path, '%08d.jpg' % idx))
        save_anno_mask(anno_file, mask_files, anno_dest_path, mask_dest_path, idx)
        idx += 1

        newimage = enhancer.enhance(0.7)
        newimage.save(os.path.join(image_dest_path, '%08d.jpg' % idx))
        save_anno_mask(anno_file, mask_files, anno_dest_path, mask_dest_path, idx)
        idx += 1
    print('Changing the brightness and contrast of images done ...')
