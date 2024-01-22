#!/usr/bin/env python
import rospy
from pymavlink import mavutil
import sys, os
import numpy as np
from std_msgs.msg import Float64MultiArray
import pickle
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument('--save',type=str, help='filename to save the data.')
args = parser.parse_args()

def vlog():
    rospy.init_node('vicon_bridge', anonymous=True)
    pub = rospy.Publisher('/vicon_estimate', Float64MultiArray, queue_size=1)

    # create a mavlink serial instance
    master = mavutil.mavlink_connection('udpin:0.0.0.0:10086')

    data = Float64MultiArray()

    data.data = [0, ] * (9 + 2 + 4 + 1)

    datastorage = []

    while not rospy.is_shutdown():
        msg = master.recv_match(blocking=False)
        if not msg:
            continue

        if msg.get_type() == 'LOCAL_POSITION_NED_COV':
            data.data[0] = msg.x / 1000.
            data.data[1] = msg.y / 1000.
            data.data[2] = msg.z / 1000.
            data.data[3] = msg.vx / 1000.
            data.data[4] = msg.vy / 1000.
            data.data[5] = msg.vz / 1000.
            data.data[6] = msg.ax / 1000.
            data.data[7] = msg.ay / 1000.
            data.data[8] = msg.az / 1000.

            # print("Coordinaes recieved")
            # use msg.covaricane to store the yaw and yaw_rate, and q
            offset = 100.
            data.data[9] = msg.covariance[0] - offset
            data.data[10] = msg.covariance[1] - offset

            data.data[11] = msg.covariance[2] - offset
            data.data[12] = msg.covariance[3] - offset
            data.data[13] = msg.covariance[4] - offset
            data.data[14] = msg.covariance[5] - offset

            now = rospy.get_rostime()
            now = now.to_sec()
            data.data[-1] = now
            pub.publish(data)

            datastorage.append(data)
            print("getting")

        elif msg.get_type() == 'ATT_POS_MOCAP':
            pass
    
    return datastorage

if __name__ == '__main__':
    datastorage = vlog()

    if args.save is not None:
        with open(f'{args.save}.pkl','wb') as file:
            pickle.dump(datastorage,file)
        print(f"saved data to {args.save}")
    else:
        print("finished vicon without saving")
