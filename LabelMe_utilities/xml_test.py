from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import os
import re
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

if __name__ == "__main__":
    anno_file = '/home/chentao/00000669.xml'
    id = 1
    tree = ET.ElementTree(file=anno_file)
    filename = tree.find('filename')
    filename.text = '%08d.jpg' % id

    for object in tree.iter('object'):
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
    tree.write('/home/chentao/%08d.xml' % id)