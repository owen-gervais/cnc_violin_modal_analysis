from json import tool
from vedo import *
import numpy as np
from math import floor
import os

class ImpactHammerPathPlanner:

    def __init__(self, mesh, stepSize, midlineOffset, yDatumOffset):
        self.mesh = mesh                                                        # Mesh Tool
        self.referencePlane = Plane(pos=(0,50, 50), sx=100, normal=(1,0,0))     # Defining a reference plane for movement
        self.bounds = {}                                                        # Populate empty dictionary for STL bound storage
        
        self.getSTLBoundaries()                                                 # Populate bounds object

        self.stepSize = stepSize                                                # Define number of steps
        self.bridgeClearanceFromCenterLine = midlineOffset                      # Define symmetrical offset from the centerline of the STL
        self.bridgeClearanceFromYDatum = yDatumOffset                           # Define offset from y datum to avoid chinrest

        self.targetLines = []                                                   # Preallocate the target lines object
        self.lL = 100                                                           # Line length to intersect the stl in two points

        self.leftIntersectionPoints = []                                        
        self.rightIntersectionPoints = []
        self.getIntersectionPoints()
        

        self.leftPts = Points(self.leftIntersectionPoints, c=(0, 0, 255), alpha=1, r=9)
        self.rightPts = Points(self.rightIntersectionPoints, c=(255, 0, 0), alpha=1, r=9)


        self.leftToolpath = Lines([[0, 0 , 0]], endPoints=[[0, 0 , 1]], c='k4', alpha=1, lw=1, dotted=False, scale=1, res=1)
        self.rightToolpath = Lines([[0, 0 , 0]], endPoints=[[0, 0 , 1]], c='k4', alpha=1, lw=1, dotted=False, scale=1, res=1)
        self.drawToolpath()

        # Intialize STL Bounding Planes for visualization
        self.xMinPlane = Plane()
        self.xMaxPlane = Plane()
        self.yMinPlane = Plane()
        self.yMaxPlane = Plane()

        # 
        self.xMinBridgeClearancePlane = Plane()
        self.xMaxBridgeClearancePlane = Plane()
        self.yMinBridgeClearancePlane = Plane()
        self.midPlane = Plane()
        
        self.setBoundingPlanes()

        self.xMachineCenter = 60 #176
        self.yMachineCenter = 0 #165


    def getSTLBoundaries(self):
        boundaryList = self.mesh.distanceTo(self.referencePlane).bounds() # Establish all of the distances to the boundaries
        axes = ["x","y","z"]
        options = ["min","max"]
        index = 0
        for axis in axes:
            for option in options:
                self.bounds[axis+"_"+option] = boundaryList[index]
                index+=1
        self.bounds["mid_plane"] = int(self.bounds["x_min"] + ((self.bounds["x_max"]-self.bounds["x_min"])/2))

    
    def setBoundingPlanes(self):
        # Min-Max X and Y planes established
        self.xMinPlane = Plane(pos=(self.bounds["x_min"],self.bounds["y_min"] + (self.bounds["y_max"]-self.bounds["y_min"])/2, self.bounds["z_min"] + (self.bounds["z_max"]-self.bounds["z_min"])/2), sx=(self.bounds["z_max"]-self.bounds["z_min"]),sy=(self.bounds["y_max"]-self.bounds["y_min"]), normal=(1,0,0), c="blue", alpha = 0.25)
        self.xMaxPlane = Plane(pos=(self.bounds["x_max"],self.bounds["y_min"] + (self.bounds["y_max"]-self.bounds["y_min"])/2, self.bounds["z_min"] + (self.bounds["z_max"]-self.bounds["z_min"])/2), sx=(self.bounds["z_max"]-self.bounds["z_min"]),sy=(self.bounds["y_max"]-self.bounds["y_min"]), normal=(1,0,0), c="blue", alpha = 0.25)
        self.yMinPlane = Plane(pos=(self.bounds["x_min"] + (self.bounds["x_max"]-self.bounds["x_min"])/2,self.bounds["y_min"], self.bounds["z_min"] + (self.bounds["z_max"]-self.bounds["z_min"])/2), sx=(self.bounds["z_max"]-self.bounds["z_min"]),sy=(self.bounds["x_max"]-self.bounds["x_min"]), normal=(0,1,0), c="blue", alpha = 0.25)
        self.yMaxPlane = Plane(pos=(self.bounds["x_min"] + (self.bounds["x_max"]-self.bounds["x_min"])/2,self.bounds["y_max"], self.bounds["z_min"] + (self.bounds["z_max"]-self.bounds["z_min"])/2), sx=(self.bounds["z_max"]-self.bounds["z_min"]),sy=(self.bounds["x_max"]-self.bounds["x_min"]), normal=(0,1,0), c="blue", alpha = 0.25)
        
        # Setup the Bridge clearance planes
        self.xMinBridgeClearancePlane = Plane(pos=(self.bounds["x_min"] + ((self.bounds["x_max"]-self.bounds["x_min"])/2) - self.bridgeClearanceFromCenterLine,self.bounds["y_min"] + (self.bounds["y_max"]-self.bounds["y_min"])/2, self.bounds["z_min"] + (self.bounds["z_max"]-self.bounds["z_min"])/2), sx=(self.bounds["z_max"]-self.bounds["z_min"]) + 10,sy=(self.bounds["y_max"]-self.bounds["y_min"]), normal=(1,0,0), c="red", alpha = 0.25)
        self.xMaxBridgeClearancePlane = Plane(pos=(self.bounds["x_min"] + ((self.bounds["x_max"]-self.bounds["x_min"])/2) + self.bridgeClearanceFromCenterLine,self.bounds["y_min"] + (self.bounds["y_max"]-self.bounds["y_min"])/2, self.bounds["z_min"] + (self.bounds["z_max"]-self.bounds["z_min"])/2), sx=(self.bounds["z_max"]-self.bounds["z_min"]) + 10,sy=(self.bounds["y_max"]-self.bounds["y_min"]), normal=(1,0,0), c="red", alpha = 0.25)
        self.yMinBridgeClearancePlane = Plane(pos=(self.bounds["x_min"] + (self.bounds["x_max"]-self.bounds["x_min"])/2,self.bounds["y_min"] + self.bridgeClearanceFromYDatum, self.bounds["z_min"] + (self.bounds["z_max"]-self.bounds["z_min"])/2), sx=(self.bounds["z_max"]-self.bounds["z_min"]),sy=(self.bounds["x_max"]-self.bounds["x_min"]), normal=(0,1,0), c="blue", alpha = 0.25)
        
        # Mid Plane

    def getIntersectionPoints(self): 
        for i in range(int(self.bounds["y_min"]), int(self.bounds["y_max"])+1, self.stepSize):
            for k in range(int(self.bounds["mid_plane"]), int(self.bounds["x_max"]) + 1, self.stepSize):
                if k > (int(self.bounds["mid_plane"]) + self.bridgeClearanceFromCenterLine):
                    p1, p2 = (k,i,0), (k,i,self.lL)
                    ipts_coords = violin.intersectWithLine(p1, p2)
                    if np.any(ipts_coords):
                        self.targetLines.append([p1,p2])
                        self.rightIntersectionPoints.append(ipts_coords[1])
            
            if (i > self.bounds["y_min"]+ self.bridgeClearanceFromYDatum):
                for j in range(int(self.bounds["mid_plane"]), int(self.bounds["x_min"])-1, -self.stepSize):
                    if j < (int(self.bounds["mid_plane"]) - self.bridgeClearanceFromCenterLine):
                        p1, p2 = (j,i,0), (j,i,self.lL)
                        ipts_coords = violin.intersectWithLine(p1, p2)
                        if np.any(ipts_coords):
                            self.targetLines.append([p1,p2])
                            self.leftIntersectionPoints.append(ipts_coords[1]) 
            
                

    def generateGCODE(self, points, writeFile = False, fileName = "points.gcode", left=False, right=False, hammerOffset=False):
        '''
        Generates the GCODE assuming a series of G0 Linear movements and writes out to a designated file
        
            Inputs: 
                writeFile: type(BOOLEAN) -> Indicate whether to write output to file
                fileName: type(STRING) -> Name of file for gcode output
        ________________________________________________________________________________________________
        '''
        axes = ["X","Y"]
        file = open(fileName, "w") # Create the file object with append permissions
        x_offset = abs(points[0][0])
        y_offset = abs(points[0][1])
        file.write("G28 C;\nG38.3 Z100;\nG28 Y;\nG28 X;\nG0 X{} Y{};\nG4 P10000;\nG28 Z;\n".format(self.xMachineCenter, 0))
        if left:
            file.write("G0 C0;\n")
        elif right:
            file.write("G0 C180;\n")
        for point in points: # Iterate through all points
            command = "G0 " # Reset the command string
            for axis in axes:
                if axis == "X":
                    toolhead_offset = x_offset + self.xMachineCenter
                    if left and hammerOffset:
                        toolhead_offset = toolhead_offset - 125
                    if right and hammerOffset:
                        toolhead_offset = toolhead_offset + 125
                if axis == "Y":
                    toolhead_offset = y_offset
                command += axis + str(round(point[axes.index(axis)],1)+toolhead_offset) + " "
            command = command[:-1] + ";"
            if writeFile:
                file.write(command + '\n')
                impact_command = ""
                for i in range(0,3):
                    impact_command += "G4 P2000;\nM42 P47 S255;\nG4 P300;\nM42 P47 S0;\n"
                impact_command += "G4 P2000;\n"
                file.write(impact_command)


    def drawToolpath(self):
        ''' 
        Creates Vedo Line objects visualizing the toolpaths of the left and right approaches to the violin

            Inputs: NONE
        __________________________________________________________________________________________________
        '''
        self.leftToolpath = Lines(self.leftIntersectionPoints[0:-1], self.leftIntersectionPoints[1:], c=(255, 0, 0), alpha=1)
        self.rightToolpath = Lines(self.rightIntersectionPoints[0:-1], self.rightIntersectionPoints[1:], c=(0, 0, 255), alpha=1)

    def outputSTLTraits(self):
        '''
        Getter function in order to grab the STL characteristics

            INPUTS: NONE
        '''
        print("x_min: {}".format(floor(self.bounds["x_min"])))
        print("x_max: {}".format(floor(self.bounds["x_max"])))
        print("y_min: {}".format(floor(self.bounds["y_min"])))
        print("y_max: {}".format(floor(self.bounds["y_max"])))
        print("z_min: {}".format(floor(self.bounds["z_min"])))
        print("z_max: {}".format(floor(self.bounds["z_max"])))
        print("midline: {}".format(floor(self.bounds["mid_plane"])))


    def render(self, showBoundingPlanes = False):
        if showBoundingPlanes:
            #show(self.leftPts, self.rightPts, self.rightToolpath, self.leftToolpath, self.mesh.c("yellow"), self.xMinPlane, self.xMaxPlane, self.yMinPlane, self.yMaxPlane, self.xMinBridgeClearancePlane, self.xMaxBridgeClearancePlane, self.yMinBridgeClearancePlane, axes=True)
            show(self.rightPts, self.rightToolpath, self.mesh.c("yellow"), self.xMinPlane, self.xMaxPlane, self.yMinPlane, self.yMaxPlane, self.xMinBridgeClearancePlane, self.xMaxBridgeClearancePlane, self.yMinBridgeClearancePlane, axes=True)
        else: 
            show(self.mesh, axes=True)



if __name__ == "__main__":
    violin = Mesh("vrev4.stl")
    path = ImpactHammerPathPlanner(violin, stepSize=40, midlineOffset=20, yDatumOffset=70)
    path.outputSTLTraits()
    path.generateGCODE(path.rightIntersectionPoints, writeFile=True, fileName = "rightPoints.gcode", right=True, hammerOffset=True)
    path.generateGCODE(path.leftIntersectionPoints, writeFile=True, fileName = "leftPoints.gcode", left=True, hammerOffset=True)
    path.drawToolpath()
    path.render(showBoundingPlanes=True)
