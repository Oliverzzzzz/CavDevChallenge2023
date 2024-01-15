class CavControls:
    
    targetVel_mps = 0
    egoVehXVel_mps = 0
    
    accelPdl_pct = 0
    decelPdl_pct = 0
    
    def __init__(self):
        pass
    
    def setTargetVel_mps(self, vel): self.targetVel_mps = vel
    def setEgoVehXVel(self, egoVehXVel_mps): self.egoVehXVel_mps = egoVehXVel_mps
    
    def getAccelPdl_pct(self): return self.accelPdl_pct
    def getDecelPdl_pct(self): return self.decelPdl_pct
    
    def executeLongitudinalControl(self):
        
        # WRITE AN ALGORITHM THAT USES THE TARGET VELOCITY TO GENERATE AN ACCEL/BRAKE PEDAL POSITION TO CONTROL THE VEHICLE
        # IMLPEMENT YOUR CODE HERE! 
        
        # accelPdl_pct = 0 # accelerator pedal percentage in range [0, 1]
        # decelPdl_pct = 0 # brake pedal percentage in range [0, 1]
        
        # self.accelPdl_pct = accelPdl_pct
        # self.decelPdl_pct = decelPdl_pct

        # Control algorithm
        velocity_difference = self.targetVel_mps - self.egoVehXVel_mps
        
        acceleration_threshold = 0.1  # m/s^2
        deceleration_threshold = -0.1  # m/s^2
        max_pedal_pct = 1.0  # 100%
        
        if velocity_difference > acceleration_threshold:
            self.accelPdl_pct = min(max_pedal_pct, velocity_difference / self.targetVel_mps)
            self.decelPdl_pct = 0
        elif velocity_difference < deceleration_threshold:
            self.decelPdl_pct = min(max_pedal_pct, -velocity_difference / self.targetVel_mps)
            self.accelPdl_pct = 0
        else:
            self.accelPdl_pct = 0
            self.decelPdl_pct = 0