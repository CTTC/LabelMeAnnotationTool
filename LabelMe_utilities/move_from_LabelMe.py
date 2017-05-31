#!/usr/bin/env python
"""
Move all labels(Annotations, Masks), Scribbles, and Images from
LabelMeAnnotationTool to the current folder containing this script

Author: Tao Chen
Email: chentao904@163.com
Date: 2017.05.16
"""

from __future__ import print_function
import shutil
import os
import errno

def ignore_function(ignore):
    def _ignore_(path, names):
        ignored_names = []
        if ignore in names:
            ignored_names.append(ignore)
        return set(ignored_names)
    return _ignore_

def copy(src, dest):
    try:
        # shutil.copytree(src, dest, ignore=ignore_function('specificfile.file'))
        # shutil.copytree(src, dest, ignore=shutil.ignore_patterns('*.py', '*.sh', 'specificfile.file'))
        shutil.copytree(src, dest)
    except OSError as e:
        print('Error occurs when copy %s to %s' % (src, dest))
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(src, dest)
        else:
            print('Directory not copied. Error: %s' % e)

if __name__ == "__main__":
    root_path = '/var/www/html/LabelMeAnnotationTool'
    anno_path = os.path.join(root_path, 'Annotations', 'example_folder')
    image_path = os.path.join(root_path, 'Images', 'example_folder')
    mask_path = os.path.join(root_path, 'Masks', 'example_folder')
    scribble_path = os.path.join(root_path, 'Scribbles', 'example_folder')

    cur_dir = os.path.dirname(os.path.realpath(__file__))
    dest_dir = os.path.join(cur_dir, 'Labels3')
    anno_dest_path = os.path.join(dest_dir, 'Annotations')
    image_dest_path = os.path.join(dest_dir, 'Images')
    mask_dest_path = os.path.join(dest_dir, 'Masks')
    scribble_dest_path = os.path.join(dest_dir, 'Scribbles')
    dest_folders = [anno_dest_path, image_dest_path, mask_dest_path, scribble_dest_path]
    for folder in dest_folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print('Deleting the existing label folder: %s' % folder)

    print('Starting copying labels ...')
    copy(anno_path, anno_dest_path)
    copy(image_path, image_dest_path)
    copy(mask_path, mask_dest_path)
    copy(scribble_path, scribble_dest_path)
    print('Copying done ...')

