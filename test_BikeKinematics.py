from BikeKinematics import BikeKinematics
from EstimatedPose import EstimatedPose
import copy
import math

EPSILON = .0001

def almost_zero(value):
    return abs(value) < EPSILON

def test_BikeTurns():
    bike = get_default_bike()
    #turn left, then turn right the same amount. HSould be facing back to start
    new_pose = bike.estimate(12, math.pi/4, 250, 100)
    new_pose = bike.estimate(12, -math.pi/4, 250, 100)
    assert new_pose.heading == 0

def get_default_bike():

    pose = EstimatedPose()
    bike = BikeKinematics(0.2, 1.0, 512, copy.copy(pose))
    return bike

def test_bike_wheels():
    bike = get_default_bike()
    #confirm that with a default ike, 512 ticks gives us a full turn of the travel
    assert bike.get_front_wheel_travel(512) == math.pi * .2 * 2

    #now confirm a 1 meter diameter wheel goes pi distane in one turn
    pose = EstimatedPose()
    bike2 = BikeKinematics(.5, 1.0, 512, pose)
    assert bike2.get_front_wheel_travel(512) == math.pi

def test_turning_radius():
    bike = get_default_bike();
    #test that a 90 degree turn to the left has a radius equal to the hub distance
    assert bike.get_turning_radius(math.pi/2) == bike.hub_distance
    # a 30 degree turn should yield a radius twice the hub distance
    assert abs(bike.get_turning_radius(math.pi/6) -  bike.hub_distance * 2 ) < .004

def test_half_circle():
    

    #Make a bike with front diameter of 1, so the wheel will go pi distance.
    pose = EstimatedPose()
    assert pose.heading ==0
    bike = BikeKinematics(.5, 1.0, 512 , pose)

    #confirm the turning radius is 2
    assert almost_zero( bike.get_turning_radius(math.pi/6) - 2)
    #onfirm if we go a revolution of the wheel, we wil go pi radians
    assert almost_zero( bike.get_radians_travelled(math.pi/6 , 2*math.pi) - math.pi)
    
    rpose = bike.estimate(1, math.pi/6, 512 *2, 0)

    assert almost_zero( rpose.heading - math.pi )
    assert almost_zero( rpose.x )

    #the front wheel goes 4 units up, the back wheel takes a slightly shorter path
    assert  rpose.y  < 4

def test_full_circle_left():
 
    pose = EstimatedPose()
    assert pose.heading ==0
    bike = BikeKinematics(.5, 1.0, 512, pose)
    rpose = bike.estimate(1, math.pi/6, 512*4, 0)

    assert rpose.heading  < EPSILON
    assert almost_zero(rpose.x)
    assert almost_zero(rpose.y)

def test_full_circle_right():
 
    pose = EstimatedPose()
    bike = BikeKinematics(.5, 1.0, 512, pose)
    rpose = bike.estimate(1, -math.pi/6, 512*4, 0)

    assert rpose.heading  < EPSILON
    assert almost_zero(rpose.x)
    assert almost_zero(rpose.y)

def test_heading_normalization():
    bike = get_default_bike()
    assert almost_zero(bike.normalize_heading(math.pi  + 1 ) + math.pi - 1)
    assert almost_zero(bike.normalize_heading(3/2 * math.pi   ) + math.pi /2 ) 
    assert almost_zero(bike.normalize_heading(3 * math.pi ) - math.pi )
