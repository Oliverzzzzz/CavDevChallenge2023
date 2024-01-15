import numpy as np
from sklearn.cluster import DBSCAN

class CavPerception:
    
    radarData = None #2d numpy array where each row represents a radar point in the form [velocity, azimuthAngle, altitude, depth]
    lidarData = None #2d numpy array where each row represents a point of the point cloud in the form [xPosition, yPosition, zPosition]
    
    leadVehValidity = False
    leadVehRelXPos_m = 0
    leadVehRelXVel_mps = 0
    egoVehXVel_mps = 0
    
    def __init__(self):
        pass
    
    def processAndSetRadarData(self, rawRadarData): 
        self.radarData = np.reshape(rawRadarData, (-1, 4))
        
    def processAndSetLidarData(self, rawLidarData): 
        self.lidarData = np.reshape(rawLidarData, (-1, 3))
    
    def setEgoVehXVel(self, egoVehXVel_mps): self.egoVehXVel_mps = egoVehXVel_mps
    
    def getLeadVehValidity(self): return self.leadVehValidity
    def getLeadVehRelXPos_m(self): return self.leadVehRelXPos_m
    def getLeadVehRelXVel_mps(self): return self.leadVehRelXVel_mps
    
    def processAndFuseSensorData(self):
        
        # WRITE AN ALGORITHM THAT USES THE RADAR DATA (AND OPTIONALLY LIDAR DATA) TO DETERMINE THE POSITION AND VELOCITY OF THE LEAD VEHICLE (IF THERE IS ONE IN SENSOR RANGE)
        # IMLPEMENT YOUR CODE HERE! 
        
        # self.leadVehValidity = False # validity flag (is there a lead vehicle in range?)
        # self.leadVehRelXPos_m = 0 # relative position of the lead vehicle wrt ego vehicle (meters)
        # self.leadVehRelXVel_mps = 0 # relative velocity of the lead vehicle wrt ego vehicle (meters/sec)

        if self.radarData is None or len(self.radarData) == 0:
            self.leadVehValidity = False
            return

        # Filter radar points that are in front of the vehicle
        front_radar_points = np.array([point for point in self.radarData if self.isPointInFront(point)])
        if len(front_radar_points) == 0:
            self.leadVehValidity = False
            return

        # Cluster radar points using DBSCAN
        clusters = DBSCAN(eps=5, min_samples=3).fit(front_radar_points[:, :2])  # Using first two columns (e.g., x and y coordinates)

        # Identify lead vehicle cluster
        lead_vehicle_cluster = self.identifyLeadVehicleCluster(front_radar_points, clusters.labels_)

        if lead_vehicle_cluster is not None:
            # Calculate relative position and velocity
            self.leadVehRelXPos_m, self.leadVehRelXVel_mps = self.calculateRelPosAndVel(lead_vehicle_cluster)
            self.leadVehValidity = True
        else:
            self.leadVehValidity = False

    def isPointInFront(self, point):
        # Example logic: Check if the azimuth angle is within a certain range
        azimuth_angle = point[1]  # Assuming second value is the azimuth angle
        return -45 <= azimuth_angle <= 45  # Adjust angle range as needed

    def identifyLeadVehicleCluster(self, points, labels):
        unique_labels = set(labels)
        if -1 in unique_labels:
            unique_labels.remove(-1)  # Remove noise label

        # Find the nearest cluster
        nearest_cluster = None
        min_distance = float('inf')
        for label in unique_labels:
            cluster_points = points[labels == label]
            distance = np.mean(cluster_points[:, 3])  # Assuming fourth value is distance
            if distance < min_distance:
                min_distance = distance
                nearest_cluster = cluster_points

        return nearest_cluster

    def calculateRelPosAndVel(self, cluster):
        avg_x_pos = np.mean(cluster[:, 0])  # Assuming x position is the first value
        avg_velocity = np.mean(cluster[:, 2])  # Assuming velocity is the third value
        return avg_x_pos, avg_velocity

        
