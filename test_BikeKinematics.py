from BikeKinematics import BikeKinematics
from EstimatedPose import EstimatedPose
import copy
import math

def test_BikeTurns():
    bike = get_default_bike()
    new_pose = bike.estimate(12, 250, math.pi/4, 100)
    new_pose = bike.estimate(12, 250, -math.pi/4, 100)
    assert new_pose.heading == 0

def test_BikeCircles():
    bike = get_default_bike() 
    new_pose = bike.estimate(12, 512*6, -math.pi/4, 100)
    assert new_pose.heading <.00089

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
