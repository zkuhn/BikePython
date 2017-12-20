class EstimatedPose :

    def __init__(self,x=0, y=0, heading=0):
        """Representation of an arbitrary item in 2d space."""
        self.x = x
        self.y = y
        self.heading = heading
    
    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y) + " heading: " + str(self.heading) + "\n"

