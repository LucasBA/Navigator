"""Totem Search Pattern.
    INPUTS:
        -GPS coordinate of totem area on first iteration, then the previous iterations center point
        -buoy locations from perception
    OUTPUTS:
        -waypoints for iteration of search pattern
            (attempts approximate the center of the buoy field and to move in a circle about this point)    
    Approach:
        -Arive at given GPS location
        -Begin observing for totems and store location and color in a list as they are found
            -Rotate 2pi
                -Store list of unit vectors representing directions of detected buoys 
                -Calculate the sum of the vectors and multiply by some scalar
            -Travel to point represented by calculated vector and drive in a circle where r=10m
                -Take list of detected buoys 
                -Calculate the center of mass of the detected buoys
            -Repeat with r=20,30,0,10,20,30... until all requested totems are found
"""
import numpy as np
import rospy
import tf
from geometry_msgs.msg import PoseArray, Point
from std_msgs.msg import Int8



class TotemSearch:
    def __init__(self):
        self.radius = (0,10,20,30)
        self.gain = 1 #tune this
        self.search_service = rospy.Service('mission/totem_search', TotemSearch, self.get_circle)


    def get_circle(self,srv):
        """Take radius and returns waypoints with heading along the circle."""
        if srv.iter == 0:
            center_point = srv.center
            direction = [sum(i) for i in zip(*srv.buoys)]
            center_point = direction*self.gain+center_point
        if self.radius[srv.iter] == 0:
            spin = []
            for i in range(0,4):
                eul = [0.0,0.0,i*np.pi/2]
                quat = quaternion = tf.transformations.quaternion_from_euler(eul)
                new_point = [center_point, quat]
                spin.append(new_point)
                waypoints = spin
            return waypoints
        else:          
            number_of_points = floor(self.radius[srv.iter]*4/10)
            circle = []
            angle = 0
            for i in number_of_points:
                angle = 2*np.pi/number_of_points + angle
                eul = angle+np.pi/2
                quat = quaternion = tf.transformations.quaternion_from_euler(eul)
                point = (self.radius[srv.iter]*[np.cos(angle), np.sin(angle)],quat)
                circle.append(point)
                waypoints = circle
            return waypoints
    
    

def main(args):
    ts = TotemSearch()
    rospy.spin()

if __name__ == '__main__':
    rospy.init_node('totem_search')
    main(sys.argv)