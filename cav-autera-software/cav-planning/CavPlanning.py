class CavPlanning:
    
    leadVehValidity = 0
    leadVehRelXPos_m = 0
    leadVehRelXVel_mps = 0
    
    accSetSpd_mps = 0
    
    targetVel_mps = 0
    
    def __init__(self):
        pass
    
    def setLeadVehData(self, validity, relDist, relVel): 
        self.leadVehValidity = validity
        self.leadVehRelXPos_m = relDist
        self.leadVehRelXVel_mps = relVel
        
    def setAccSetSpd_mps(self, accSetSpd): self.accSetSpd_mps = accSetSpd 
    
    def getTargetVel_mps(self): return self.targetVel_mps
    
    def determineTargetVelocity(self):
        
        # WRITE AN ALGORITHM THAT USES THE LEAD VEHICLE DATA TO PLAN A TARGET VELOCITY FOR THE EGO VEHICLE TO FOLLOW
        # IMLPEMENT YOUR CODE HERE! 
        
        # targetVel_mps = 0 # ego vehicle target velocity (m/s)
        
        # Constants for the algorithm
        SAFE_FOLLOWING_DISTANCE = 2.0  # meters
        MAX_ACCELERATION = 2.0         # m/s^2
        MAX_DECELERATION = -3.0        # m/s^2
        TIME_GAP = 1.5                 # seconds
        
        if self.leadVehValidity:
            # Calculate the desired gap based on the current speed and a time gap
            desired_gap = self.accSetSpd_mps * TIME_GAP
            
            # Calculate the difference in velocity between the ego and lead vehicle
            rel_speed_diff = self.leadVehRelXVel_mps - self.accSetSpd_mps
            
            # Check if the ego vehicle is too close or too far from the lead vehicle
            if self.leadVehRelXPos_m < desired_gap - SAFE_FOLLOWING_DISTANCE:
                # If it is too close, then decelerate
                acceleration = max(rel_speed_diff / TIME_GAP, MAX_DECELERATION)
            elif self.leadVehRelXPos_m > desired_gap + SAFE_FOLLOWING_DISTANCE:
                # If it is too far, then accelerate
                acceleration = min(rel_speed_diff / TIME_GAP, MAX_ACCELERATION)
            else:
                # Maintain current speed
                acceleration = 0
            
            # Calculate new target velocity
            targetVel_mps = self.accSetSpd_mps + acceleration * TIME_GAP
        else:
            # If lead vehicle data is invalid, maintain current set speed
            targetVel_mps = self.accSetSpd_mps

        self.targetVel_mps = targetVel_mps