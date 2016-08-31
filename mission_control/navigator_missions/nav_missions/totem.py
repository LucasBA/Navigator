#!/usr/bin/env python
import txros  # txros is required for all missions since it's the backbone on which we build missions.



@txros.util.cancellableInlineCallbacks
def main(navigator):
    totem_list = navigator._node_handle.get_service_client('/mission/totem/list', SetBool)
    totem_list = navigator._node_handle.get_service_client('/mission/totem/find', totem_list)
    center = [0,0,0]#GPS waypoint given by competition
    #GPS frame to enu
    yield navigator.move(center).go()
    iteration = 0
    buoy_list = [0]
    while (totem_list[0]==False):
        totem_list = navigator._node_handle.get_service_client('/mission/totem/find', [totem_list,iteration])
        buoy_list = navigator._node_handle.get_service_client('/oa/buoy/find')
        waypoints = navigator._node_handle.get_service_client('/mission/totem/search', buoy_list, center)
        for i in len(waypoints):
            yield navigator.move(waypoints[i])
        iteration+=1
    for i in totem_list:
        waypoints = navigator._node_handle.get_service_client('/mission/totem/search', buoy_list, totem_list[i])
        for i in len(waypoints):
            yield navigator.move(waypoints[i])


    print "Done!"