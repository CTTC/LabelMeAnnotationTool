#!/usr/bin/env python
"""
Merge images into one folder and 
separating them into several evenly sized chunks

Author: Tao Chen
Email: chentao904@163.com
Date: 2017.05.25
"""

from __future__ import print_function
import shutil
import os
import re
import errno
import numpy as np

if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    src_path = os.path.join(cur_dir, 'Resized_Cameras')
    print('Start separating images ...')
    src_files = os.listdir(src_path)
    num_sep = 2
    tgt_folders = []
    for idx in xrange(num_sep):
        folder = os.path.join(cur_dir, '%d'%idx)
        if not os.path.exists(folder):
            os.makedirs(folder)
        else:
            shutil.rmtree(folder)
            os.makedirs(folder)
        tgt_folders.append(folder)
    num_files = len(src_files)
    sep_chunk = np.array_split(range(num_files), num_sep)
    for index, chunk in enumerate(sep_chunk):
        chunk = chunk.tolist()
        for idx in chunk:
            folder = tgt_folders[index]
            src = os.path.join(src_path, '%08d.jpg' % idx)
            dst = os.path.join(folder)
            shutil.copy2(src, dst)
    print('Separating images done ...')







