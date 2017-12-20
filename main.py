from BikeKinematics import BikeKinematics
from EstimatedPose import EstimatedPose
import math
import copy 

#a default pose is at 0,0 and points "right"
pose = EstimatedPose();

# make a bike with a .2 meter tall front wheel, 1.0meters between hubs
# that counts 512 ticks per revolution of the front wheel
#start it at the default pose and heading
bike_test = BikeKinematics(.2, 1.0, 512, copy.copy(pose) )

#turn 45 degres to the left and move forward half a rev
new_pose = bike_test.estimate(15, math.pi/4, 250, 12)

print(new_pose)
#now turn 45 degrees back to the right and move forward half a rev
new_pose = bike_test.estimate(15, -math.pi/4, 250, 12)

#we should have moved positive x direction mostly and up a bit, 
#and be back on the original heading
print(new_pose)

print(pose)
