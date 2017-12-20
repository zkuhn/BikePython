from EstimatedPose import EstimatedPose
class BikeKinematics :

    def _init_(self, front_radius, hub_distance, ticks_per_revolution, starting_pose):
        """Create a bike model with the startingPose"""
        self.front_radius = front_Radius
        self.hub_distance = hub_distance
        self.ticks_per_revolution = ticks_per_revolution
        self.estimated_pose = starting_pose
    
    def get_pose(self):
        return self.estimated_pose

    def get_front_wheel_travel(self, ticks):
        rotation = ticks/self.ticks_per_revolution
        return rotation * self.get_front_circumfrence()

    def get_front_circumfrence(self) :
        return self.frontRadius * 2 * math.pi

    def estimate(self, time, steering_angle, encoder_ticks, angular_velocity):

        total_front_distance = self.get_front_wheel_travel(encoder_ticks)

        #default case of moving in a stright line
        if steering_angle > -.0001 and steering_angle < .0001 :
            self.estimated_pose.x += math.cos(self.estimated_pose.current_heading) * total_front_distance
            self.estimated_pose.y += math.sin(self.estimated_pose.current_heading) * total_front_distance
            return self.estimated_pose
        
        steering_radius = self.get_turning_radius(steering_angle)
        radians_travelled = total_front_distance / steering_radius

        new_heading = self.estimated_pose.heading + radians_travelled

        #cheat here a bit and use a negative turn radius for right hand turns..
        #it makes our travel vectors correct based on left/right turning
        rear_wheel_turn_radius = self.hub_distance / math.tan(steering_angle);

        #sanity check.. facing south making a left turn to head north 
        # sin(pi/2) - sin (-pi/2) = 1 - (-1) = 2 .. 
        # a radius 1 half circle moves 2 units positive x direction - check
        travel_vector_x = ( math.sin(new_heading) - math.sin(self.estimated_pose.heading) ) * rear_wheel_turn_radius
        travel_vector_y = - (math.cos(new_heading) - math.cos(self.estimated_pose.heading) ) * rear_wheel_turn_radius
        
        return self.estimated_pose


    def get_turning_radius(self, steering_angle) :

        sin_steer = math.sin(steering_angle)
        return self.hub_distance / sin_steer

    def normalize_heading(heading):
        
        if heading > math.pi :
            return normalize_heading(heading - (2 * math.pi) )
        if heading <= -math.pi :
            return normalize_heading(heading + (2 * math.pi) )
        return heading;

    def get_turning_radius(steering_angle):
        """Calculates the radius of the circle the front wheel traces while travelling in a turn
        """

        sin_steer = math.sin(steering_angle)
        return self.hub_distance / sin_steer



