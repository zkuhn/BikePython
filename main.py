from BikeKinematics import BikeKinematics
from EstimatedPose import EstimatedPose
import math

pose = EstimatedPose();

bike_test = BikeKinematics(.2, 1.0, 512, pose )

#turn 45 degres to the left
new_pose = bike_test.estimate(15, math.pi/4, 250, 12)

print(new_pose)
#now turn 45 degrees back to the right
new_pose = bike_test.estimate(15, -math.pi/4, 250, 12)

#we should have moved right and up, and be back on the original heading
print(new_pose)
