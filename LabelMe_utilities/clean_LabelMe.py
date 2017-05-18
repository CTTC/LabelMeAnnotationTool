#!/usr/bin/env python
"""
Remove all labels(Annotations, Masks) and Scribbles in LabelMeAnnotationTool
Or remove labels corresponding to user-specified images 

Author: Tao Chen
Email: chentao904@163.com
Date: 2017.05.16
"""

from __future__ import print_function
import shutil
import os
import glob

if __name__ == "__main__":
    root_path = '/var/www/html/LabelMeAnnotationTool'
    anno_path = os.path.join(root_path, 'Annotations', 'example_folder')
    image_path = os.path.join(root_path, 'Images', 'example_folder')
    mask_path = os.path.join(root_path, 'Masks', 'example_folder')
    scribble_path = os.path.join(root_path, 'Scribbles', 'example_folder')
    tmp_anno_path = os.path.join(root_path, 'annotationCache', 'TmpAnnotations', 'example_folder')
    all_input = raw_input('Do you want to delete all labels? (y/n)')
    if all_input == 'y':
        print('Deleting all labels ...')
        folders = [anno_path, mask_path, scribble_path, tmp_anno_path]
        for folder in folders:
            files = os.listdir(folder)
            for f in files:
                os.remove(os.path.join(folder, f))
        print('Deleting all labels done ...')
    elif all_input == 'n':
        input = raw_input('Enter the specific image numbers whose labels you wanna delete separated by commas:')
        input_list = input.split(',')
        raw_numbers = [x.strip() for x in input_list]
        for number in raw_numbers:
            try:
                number = int(number)
                print('Deleting labels corresponding to image %d' % number)
                anno_file = os.path.join(anno_path, '%08d.xml' % number)
                mask_files = glob.glob("%s/%08d_mask*.png" % (mask_path, number))
                scribble_files = glob.glob("%s/%08d_scribble*.png" % (scribble_path, number))
                files_to_delete = mask_files + scribble_files
                files_to_delete.append(anno_file)
                for fileD in files_to_delete:
                    print('Deleting file %s' % fileD)
                    os.remove(fileD)
            except:
                print('%s is not an integer, ignoring it...' % number)
        print('Deleting labels done ... ')

