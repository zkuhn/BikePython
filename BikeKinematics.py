from EstimatedPose import EstimatedPose
import math

class BikeKinematics :

    def __init__(self, front_radius, hub_distance, ticks_per_revolution, starting_pose):
        """Create a bike model with the startingPose
        The starting pose (EstimatedPose) represents the pose of the rear hub of the bicycle.
        """
        self.front_radius = front_radius
        self.hub_distance = hub_distance
        self.ticks_per_revolution = ticks_per_revolution
        self.estimated_pose = starting_pose
    

    def get_front_wheel_travel(self, ticks):
        """ Circumfrence of the wheel times the ticks per revolution ratio.
        """
        #in python 2.x need to convert to float first
        rotation = float (ticks) / self.ticks_per_revolution
        return rotation * self.get_front_circumfrence()

    def get_front_circumfrence(self) :
        """General formula for a circle's perimiter
        """
        return self.front_radius * 2 * math.pi

    def estimate_no_effects(self,  steering_angle, encoder_ticks):
        """Return a pose that shows the bike's position after movement.
        Don't actually move the bike though.
        The trig for this just uses SOH CAH TOA to measure unit circle 
        movement, then scales it to the rear wheel travel radius
        Use the negative radius and radians travelled convention for
        right hand turns. sin and tan give you the negatives back by default
        """
        total_front_distance = self.get_front_wheel_travel(encoder_ticks)

        return_pose = EstimatedPose()

        #default case of moving in a stright line
        if (steering_angle > -.0001) and (steering_angle < .0001) :
            return_pose.x = self.estimated_pose.x + math.cos(self.estimated_pose.current_heading) * total_front_distance
            return_pose.y = self.estimated_pose.y + math.sin(self.estimated_pose.current_heading) * total_front_distance
            return_pose.heading = self.estimated_pose.heading
            return return_pose
       

        radians_travelled = self.get_radians_travelled(steering_angle, total_front_distance)

        #radiasn travelled will be negative for right hand turns (neg steering radius for right turns
        new_heading = self.estimated_pose.heading + radians_travelled

        #cheat here a bit and use a negative turn radius for right hand turns..
        #it makes our travel vectors correct based on left/right turning
        rear_wheel_turn_radius = self.hub_distance / math.tan(steering_angle);


        #sanity check.. facing south making a left turn to head north 
        # sin(pi/2) - sin (-pi/2) = 1 - (-1) = 2 .. 
        # a radius 1 half circle moves 2 units positive x direction - check
        return_pose.x = self.estimated_pose.x +  ( math.sin(new_heading) - math.sin(self.estimated_pose.heading) ) * rear_wheel_turn_radius
        return_pose.y = self.estimated_pose.y + -(math.cos(new_heading) - math.cos(self.estimated_pose.heading) ) * rear_wheel_turn_radius
        return_pose.heading = self.normalize_heading(new_heading)

        return return_pose

    
    def estimate(self, time, steering_angle, encoder_ticks, angular_velocity):
        """Give an update of the rear hub pose.
        time in s
        steering angle in radians
        ticks as a count (int)
        angular velocity in rad/s
        """
        #This will track the estimate changes over time using the side effect
        #free estimate.
        self.estimated_pose = self.estimate_no_effects(steering_angle, encoder_ticks)
        return self.estimated_pose


    def get_turning_radius(self, steering_angle) :
        """ Use trig to calc the turning radius.
        draw a triangle with radius as hypotenuse to front wheel from center
        hub distance as opposite side
        line from center of turning circle to rear hub is adjacent 
        Sin steering angle = Opposite / hypotenuse
        hub_distance = opposite
        radius = hypotenuse
        radius = opposite / (opposite/hypotenuse) - opposites cancel
        math nicely works out that right turns return negative numbers.
        invalid for zero turn angle (straight line, not a circle)
        """
        sin_steer = math.sin(steering_angle)
        return self.hub_distance / sin_steer
    
    def get_radians_travelled(self, steering_angle, total_front_distance ) :

        steering_radius = self.get_turning_radius(steering_angle)
        return total_front_distance / steering_radius

    def normalize_heading(self,heading):
        """For very long turns, resolve the heading to between +pi and - pi.
        Unless driving in cirles for a long long time, this will likeley
        ever only be subtracting or adding 2 pi one time from the heading
        it is recursive just in case though.
        """        
        if heading > math.pi :
            return self.normalize_heading(heading - (2 * math.pi) )
        if heading <= -math.pi :
            return self.normalize_heading(heading + (2 * math.pi) )
        return heading;




