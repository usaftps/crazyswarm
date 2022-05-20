"""Single CF: takeoff, follow absolute-coords waypoints, land."""

import numpy as np

from pycrazyswarm import Crazyswarm


Z = 1.0
Z1 = -0.25
Z2 = 0.25
GroupId1 = 1
GroupId2 = 2
TAKEOFF_DURATION = 2.5
GOTO_DURATION = 3.0
WAYPOINTS = np.array([
    (-1.0, 0.0, 0.),
    (0.0, 1.0, 0.),
    (1.0, 0.0, 0.),
    (0.0, -1.0, 0.),
])


def main():
    swarm = Crazyswarm(crazyflies_yaml="../launch/TPSCrazyflies.yaml")    
    timeHelper = swarm.timeHelper
    cfs = swarm.allcfs.crazyflies
    N = len(cfs)
    colors = [(0,0,1), (0,1,0)]

    swarm.allcfs.setParam("ring/effect", 7)
    
    for cf in cfs[0:N//2]:
        cf.setGroupMask(GroupId1)
        cf.setLEDColor(*colors[0])
    for cf in cfs[N//2:]:
        cf.setGroupMask(GroupId2)
        cf.setLEDColor(*colors[1])        

    swarm.allcfs.takeoff(targetHeight=Z, duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + 1.0)
    swarm.allcfs.goTo((0, 0, Z1), 180, duration=GOTO_DURATION, groupMask=GroupId1)
    swarm.allcfs.goTo((0, 0, Z2), -180, duration=GOTO_DURATION, groupMask=GroupId2)
    timeHelper.sleep(2.0)    

    for i in range(len(WAYPOINTS)):
        swarm.allcfs.goTo(WAYPOINTS[i], yaw=0.0,
                          duration=GOTO_DURATION, groupMask=GroupId1)
        swarm.allcfs.goTo(WAYPOINTS[(i+N//2)%N], yaw=0.0,
                          duration=GOTO_DURATION, groupMask=GroupId2)        
        timeHelper.sleep(GOTO_DURATION + 1.0)

    swarm.allcfs.goTo((0, 0, Z2), 180, duration=GOTO_DURATION, groupMask=GroupId1)
    swarm.allcfs.goTo((0, 0, Z1), -180, duration=GOTO_DURATION, groupMask=GroupId2)
    timeHelper.sleep(2.0)    
        
    swarm.allcfs.land(targetHeight=0.05,
                      duration=TAKEOFF_DURATION)
    timeHelper.sleep(TAKEOFF_DURATION + 1.0)


if __name__ == "__main__":
    main()
