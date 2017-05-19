#!/usr/bin/env python
"""
Count the total number of objects with segmentation
and the number of each class

Author: Tao Chen
Email: chentao904@163.com
Date: 2017.05.16
"""

from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import os
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

def plot_bar_from_counter(counter, ax=None):
    """"
    This function creates a bar plot from a counter.

    :param counter: This is a counter object, a dictionary with the item as the key
     and the frequency as the value
    :param ax: an axis of matplotlib
    :return: the axis wit the object in it
    """

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    frequencies = counter.values()
    names = counter.keys()


    x_coordinates = np.arange(len(counter))
    ax.bar(x_coordinates, frequencies, align='center')
    for idx in xrange(len(frequencies)):
        x = x_coordinates[idx]
        y = frequencies[idx]
        ax.text(x + 3, y + 3, str(v), color='red', fontweight='bold')
    ax.xaxis.set_major_locator(plt.FixedLocator(x_coordinates))
    ax.xaxis.set_major_formatter(plt.FixedFormatter(names))
    ax.set_ylim(0, np.max(frequencies) * 1.1)

    return ax

if __name__ == "__main__":
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    label_dir = os.path.join(cur_dir, 'Refined Labels')
    anno_path = os.path.join(label_dir, 'Annotations')
    anno_list = os.listdir(anno_path)
    num_obj = 0
    classes = ['floor', 'table', 'tv']
    class_dict = dict.fromkeys(classes, 0)
    for anno_file in anno_list:
        anno_file = os.path.join(anno_path, anno_file)
        tree = ET.ElementTree(file=anno_file)

        # Only count the objects with segmentation
        for object in tree.iter('object'):
            name = object.find('name')
            seg = object.find('segm')
            deleted = object.find('deleted')
            if int(deleted.text) == 1:
                continue
            if seg is None:
                continue
            num_obj += 1
            try:
                class_dict[name.text] += 1
            except:
                print('Unkown object %s in %s' % (name.text, anno_file))

        # find all objects without caring about the segmentation
        # for elem in tree.iter(tag='name'):
        #     num_obj += 1
        #     a = elem.text
        #     try:
        #         class_dict[elem.text] += 1
        #     except:
        #         print('Unkown object %s in %s' % (elem.text, anno_file))

    print('Total number of objects: ', num_obj)
    for k, v in class_dict.items():
        print('Class [%s]: %d' % (k, v))
    plot_bar_from_counter(class_dict)
    plt.show()


