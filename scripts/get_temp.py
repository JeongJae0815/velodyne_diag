#!/usr/bin/env python
# Software License Agreement (BSD License)
#
# Copyright (c) 2008, Willow Garage, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the name of Willow Garage, Inc. nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Revision $Id$

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

import rospy
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
import urllib.request as urllib2
import json
import time
import pycurl
from std_msgs.msg import String
import numpy as np
from vlp_diag.msg import temp_msg
BASE_URL = 'http://192.168.2.201/cgi/'

def cal_temp(raw_value):
    temp = -1481.96 + np.sqrt(2.1962*np.power(10,6) + (1.8639-(raw_value*5.0/4096))/(3.88/np.power(10,6)))
    return temp

def talker():
    pub = rospy.Publisher('vlp_temp', temp_msg, queue_size=10)
    rospy.init_node('get_temp', anonymous=True)
    rate = rospy.Rate(1) # 10hz
    msg = temp_msg()
    while not rospy.is_shutdown():
        #hello_str = "hello world %s" % rospy.get_time()
        response = urllib2.urlopen(BASE_URL+'diag.json')
        if response:
            diag = json.loads(response.read())
            top_temp = cal_temp(diag['volt_temp']['top']['lm20_temp'])
            bot_temp = cal_temp(diag['volt_temp']['bot']['lm20_temp'])
            res_str = 'Sensor temperature top : %s, bottom %s' % (top_temp,bot_temp)
            msg.stamp = rospy.Time.now()
            msg.top_temp = top_temp
            msg.bot_temp = bot_temp
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
