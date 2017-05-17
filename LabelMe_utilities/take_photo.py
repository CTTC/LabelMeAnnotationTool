#!/usr/bin/env python
"""
Subscribing stereo images synchronously, and saving them

Author: Tao Chen
Email: chentao904@163.com
Date: 2017.05.16
"""

import cv2
import rospy
import numpy as np
import threading
import time
import os
import re
import sys, tty, termios
import collections
from sensor_msgs.msg import Image
import message_filters
import cv_bridge
from cv_bridge import CvBridge, CvBridgeError

FrameData = collections.namedtuple('FrameData', 'left, right')
class Camera:
    def __init__(self):
        self.lock = threading.Lock()
        self._br = cv_bridge.CvBridge()
        self._cameraRight_img = None
        self._cameraLeft_img = None
        self._meta_data = None
        self._observation_stale = True
        self.camera_l_sub = message_filters.Subscriber("/left/image_raw",
                                                       Image)
        self.camera_r_sub = message_filters.Subscriber("/right/image_raw",
                                                       Image)

        self.sync = message_filters.ApproximateTimeSynchronizer([self.camera_l_sub, self.camera_r_sub],
                                                                queue_size=1, slop=0.3)

        self.sync.registerCallback(self.sync_callback)
        time.sleep(1)

    def sync_callback(self, leftImage, rightImage):
        self.lock.acquire()
        self.cameraLeft_callback(leftImage)
        self.cameraRight_callback(rightImage)
        self._meta_data = FrameData(left=self._cameraLeft_img, right=self._cameraRight_img)
        self._observation_stale = False
        self.lock.release()
        self.end = time.time()


    def cameraLeft_callback(self, data):
        try:
            self._cameraLeft_img = self._br.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

    def cameraRight_callback(self, data):
        try:
            self._cameraRight_img = self._br.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)

    def get_camera_data(self):
        self.lock.acquire()
        if self._observation_stale:
            return_value = None
        else:
            self._observation_stale = True
            return_value = self._meta_data
        self.lock.release()
        return return_value


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

if __name__ == "__main__":
    rospy.init_node('acquire_frame_data')
    camera = Camera()
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    save_path = os.path.join(cur_dir, 'Images')
    left_path = os.path.join(save_path, 'Left')
    right_path = os.path.join(save_path, 'Right')
    if not os.path.exists(left_path):
        os.makedirs(left_path)
    if not os.path.exists(right_path):
        os.makedirs(right_path)
    files_lst = os.listdir(left_path)
    max_index = 0
    for filename in files_lst:
        fileindex_list = re.findall(r'\d+', filename)
        if not fileindex_list:
            continue
        fileindex = int(fileindex_list[0])
        if fileindex >= max_index:
            max_index = fileindex
    count = max_index + 1 if max_index > 0 else max_index
    while True:
        ch = getch()
        if ch == 's':
            frame = camera.get_camera_data()
            leftIm = frame.left
            rightIm = frame.right
            left_image_filename = os.path.join(left_path, 'L%08d.jpg' % count)
            right_image_filename = os.path.join(right_path, 'R%08d.jpg' % count)
            print('Saving images (L%08d.jpg, R%08d.jpg) to %s' % (count, count, save_path))
            cv2.imwrite(left_image_filename, leftIm)
            cv2.imwrite(right_image_filename, rightIm)
            count += 1
        elif ch == 'q':
            sys.exit()
        else:
            continue

