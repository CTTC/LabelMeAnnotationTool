#!/usr/bin/env python
"""
Merge folders Labels, Labels1, Labels2, Labels3, ...
And reindexing image_ids

Author: Tao Chen
Email: chentao904@163.com
Date: 2017.05.16
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
    dest_dir = os.path.join(cur_dir, 'Refined Labels')
    anno_dest_path = os.path.join(dest_dir, 'Annotations')
    image_dest_path = os.path.join(dest_dir, 'Images')
    mask_dest_path = os.path.join(dest_dir, 'Masks')
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.makedirs(dest_dir)
    os.makedirs(anno_dest_path)
    os.makedirs(image_dest_path)
    os.makedirs(mask_dest_path)
    relation_file = os.path.join(dest_dir, 'relation.txt')
    if os.path.exists(relation_file):
        os.remove(relation_file)

    label_dirs = glob.glob('%s/Labels*' % cur_dir)
    id = 0
    print('Merging Labels and Images ...')
    for label_dir in label_dirs:
        anno_dir = os.path.join(label_dir, 'Annotations')
        image_dir = os.path.join(label_dir, 'Images')
        mask_dir = os.path.join(label_dir, 'Masks')
        if not os.path.exists(image_dir):
            continue
        images_list = os.listdir(image_dir)
        for image in images_list:
            image_idx = image.split('.')[0]
            anno_file = os.path.join(anno_dir, '%s.xml' % image_idx)
            if not os.path.exists(anno_file):
                continue
            mask_files = glob.glob("%s/%s_mask*.png" % (mask_dir, image_idx))

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
            shutil.copy2(os.path.join(image_dir, image), os.path.join(image_dest_path, '%08d.jpg' % id))
            for mask in mask_files:
                mask_name = mask.split('/')[-1]
                new_mask = re.sub('\d\d\d\d\d\d\d\d', '%08d' % id, mask_name)
                shutil.copy2(mask, os.path.join(mask_dest_path, new_mask))
            with open(relation_file, 'a+') as f:
                f.write('%s --> %08d\n' % (image_idx, id))
            id += 1
    print('Merging done ...')






