#!/usr/bin/env python
"""
Move the images in user-specified folder to LabelMeAnnotationTool

Author: Tao Chen
Email: chentao904@163.com
Date: 2017.05.16
"""
import shutil
import os


if __name__ == "__main__":
    folder_idx = 0 # 0 or 1 or 2 or 3
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    src_dir = os.path.join(cur_dir, '%d' % folder_idx)
    dest_dir = '/var/www/html/LabelMeAnnotationTool/Images/example_folder'
    images = os.listdir(src_dir)
    dirlistfile = '/var/www/html/LabelMeAnnotationTool/annotationCache/DirLists/labelme.txt'
    if os.path.exists(dirlistfile):
        os.remove(dirlistfile)

    print('Moving files to %s'%dest_dir)
    for image in images:
        src = os.path.join(src_dir, image)
        shutil.copy2(src, dest_dir)
        with open(dirlistfile, 'a+') as f:
            f.write('example_folder,%s\n' % image)
    print('Moving files done ...')



