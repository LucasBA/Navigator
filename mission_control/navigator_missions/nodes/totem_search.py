"""Totem Search Pattern.

    WARNING:This program will continue to run until all totems are found. 
            It is the responsibility of the caller to enforce a reasonable timeout.

    INPUTS:
        -GPS coordinate of totem area (does not need to be accurate, within about 70m is fine)
        -buoy locations from perception
        -totem locations from perception
    OUTPUTS:
           -Found Totems (color and location)
           -Current Itteration
    
    Approach:
        -Arive at given GPS location
        -Begin observing for totems and store location and color in a list as they are found
            -Rotate 2pi
                -Store list of unit vectors representing directions of detected buoys 
                -Calculate the sum of the vectors and multiply by some scalar
            -Travel to point represented by calculated vector and drive in a circle where r=10m
                -Store list of unit vectors representing directions of detected buoys from the center_point
                -Calculate the sum of the vectors and multiply by some scalar
            -Repeat with r=20,30,0,10,20,30... until all requested totems are found
"""
import numpy as np
import rospy
from geometry_msgs.msg import PoseArray, Point
from std_msgs.msg import Int8



class TotemSearch:
    def __init__(self):
        self.center_point = None
        self.current_iter = 0#subscriber
        self.radius = (0,10,20,30)
        self.buoy_list = []#subscriber
        self.gain = 1 #tune this


    def calculate_center(self):
        if self.current_iter == 0:
            self.center_point = current_point#get boat position (x,y)
        else:
            direction = [sum(i) for i in zip(*self.buoy_list)]
            self.center_point = direction*self.gain+self.center_point


    def get_circle(self):
        """Take radius and returns waypoints with heading along the circle."""
        if self.radius == 0:
            spin = []
            for i in range(0,4):
                new_point = [self.center_point, [0.0,0.0,i*np.pi/2]]
                spin.append(new_point)
            return spin
        else:          
            number_of_points = self.radius*4/10
            circle = []
            angle = 0
            for i in number_of_points:
                angle = 2*np.pi/number_of_points + angle
                point = (self.radius*[np.cos(angle), np.sin(angle)],angle+np.pi/2)
                circle.append(point)
            return circle
    
    

def main(args):
    ts = TotemSearch()
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('totem_search')
    main(sys.argv)

