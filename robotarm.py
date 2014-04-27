'''
Original draw robot methods taken from:
    @author: Phil Williammee
    credits: http://www.maquinapensante.com

Optimizations and GUI changes by:
    @author: Elisha Ferrara
    @author: King Ng
    @author: Andrew Spatafora
'''

from matplotlib.widgets import Slider, Button
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def main():
    myRobot=Draw_Robot()      

class Draw_Robot():
        
    def __init__(self):
        '''variable definitions'''
        SEGMENTS = int(3) #number of segments
        #could probably make these lists instead of arrays
        self.l = np.array([0, 100, 100, 80])# actual measurements of segment length in mm
        self.w = np.array([0]*SEGMENTS,dtype=float) #horizontal coordinate
        self.z = np.array([0]*SEGMENTS,dtype=float) #vertical coordinate
        self.x = np.array([0]*SEGMENTS,dtype=float) #x axis components 
        self.y = np.array([0]*SEGMENTS,dtype=float) #y axis components
        self.a = np.array([np.pi]*SEGMENTS,dtype=float) #angle for the link, reference is previous link
        self.gripper_angle = np.array([0, -45, -90, 45, 90])#preselected gripper angles
        self.current_gripper = 2    #gripper angle selection
        self.tw = 30.0 # w axis position depth
        self.tz = 20.0 # z axis starting position height
        self.l12 = 0.0 # hypotenuse belween a1 & a2
        self.a12 = 0.0 #inscribed angle between hypotenuse, w    
        self.fig = plt.figure("CS 4TE3 Robot Simulator")  #create the frame     
        self.ax = plt.axes([0.05, 0.2, 0.90, .75], projection='3d') #3d ax panel 
        self.axe = plt.axes([0.25, 0.85, 0.001, .001])#panel for error message
        self.count = 0
        self.coords = ((20,30),(50,60),(30,40),(70,100),(70,150))
        
        self.display_error()
        self.draw_robot() 

        butval = plt.axes([0.35, 0.1, 0.1, 0.075])
        but = Button(butval, 'move')
        but.on_clicked(self.move_click)
        #error = dist(1,2);
        #print (error)

        plt.show()#end of constructor

          
 
    def move_click(self, event):

        self.tw = self.coords[self.count][0]
        self.tz = self.coords[self.count][1]

        self.count +=1
        if self.count == 5:
            self.count = 0
        self.draw_robot()
    
    #ccd alogorithm
    def ccd(self):
        distance = np.sqrt((self.tw - self.x[2]) + (self.tz - self.z[2]))
        #iterate until end effector is less than 1 point away.
        while distance > 1:
            pt = (tw,tz)
            e = (self.x[2], self.z[2])
            j = (self.x[1],self,z[1])

            temp1 = (e - j)/np.norm(e - j)
            temp2 = (pt - j)/np.norm(pt - j)
            
            angle = np.arccos(np.dot(temp1,temp2))
            #direction of rotation
            #rotation = np.cross(
        
        
       
        
            
        
            
    def display_error(self):
        self.axe.set_visible(False)
        self.axe.set_yticks([])
        self.axe.set_xticks([])
        self.axe.set_navigate(False)
        self.axe.text(0, 0, 'Arm Can Not Reach the Target!', style='oblique',
                      bbox={'facecolor':'red', 'alpha':0.5, 'pad':10}, size=20, va = 'baseline')                  
                       
    def calc_p2(self):#calculates position 2
        #self.w[3] = self.tw
        #self.z[3] = self.tz
        self.w[2] = self.tw-np.cos(np.radians(self.gripper_angle[self.current_gripper]))*self.l[3]
        self.z[2] = self.tz-np.sin(np.radians(self.gripper_angle[self.current_gripper]))*self.l[3]
        self.l12 = np.sqrt(np.square(self.w[2])+np.square(self.z[2])) 
           
    def calc_p1(self):#calculate position 1
        self.a12 = np.arctan2(self.z[2],self.w[2])#return the appropriate quadrant  
        self.a[1] = np.arccos((np.square(self.l[1])+np.square(self.l12)-np.square(self.l[2])) 
                              /(2*self.l[1]*self.l12))+self.a12
        self.w[1] = np.cos(self.a[1])*self.l[1]
        self.z[1] = np.sin(self.a[1])*self.l[1]

    def calc_x_y(self):#calc x_y Pcoordinates 
        for i in range(len(self.x)):
            self.x[i] = self.w[i]*np.cos(self.a[0])
            self.y[i] = self.w[i]*np.sin(self.a[0])
    
    def set_positions(self):#gets the x,y,z values for the line. 
        #convert arrays to lists for drawing the line
        xs = np.array(self.x).tolist()# = (self.z[0], self.z[1], self.z[2], self.z[3])
        ys = np.array(self.y).tolist()
        zs = np.array(self.z).tolist()
        self.ax.cla() #clear current axis
        #draw new lines,  two lines for "fancy" looks
        self.ax.plot(xs, ys, zs, 'o-', markersize=20, 
                     markerfacecolor="red", linewidth = 8, color="black")
        self.ax.plot(xs, ys, zs, 'o-', markersize=4, 
                     markerfacecolor="blue", linewidth = 1, color="silver")
  
    def set_ax(self):#ax panel set up
        self.ax.set_xlim3d(-200, 200)
        self.ax.set_ylim3d(-200, 200)
        self.ax.set_zlim3d(-5, 200)
        self.ax.set_xlabel('X axis')
        self.ax.set_ylabel('Y axis')
        self.ax.set_zlabel('Z axis')
        for j in self.ax.get_xticklabels() + self.ax.get_yticklabels(): #show ticks
            j.set_visible(True)
        self.ax.set_axisbelow(True) #send grid lines to the background
        
    def get_angles(self): #get all of the motor angles see diagram
        self.a[2] = np.arctan((self.z[2]-self.z[1])/(self.w[2]-self.w[1]))-self.a[1]
        #self.a[3] = np.deg2rad(self.gripper_angle[self.current_gripper])-self.a[1]-self.a[2]  
        angles = np.array(self.a).tolist()
        return angles
        
    def draw_robot(self):#draw and update the 3D panel
        self.calc_p2() 
        self.calc_p1() 
        self.calc_x_y()
        if self.l12 < (self.l[1]+self.l[2]):#check boundaries 
            self.axe.set_visible(False)#turn off error message panel
            self.set_positions()
            self.set_ax()
            #print np.around(np.rad2deg(self.get_angles()),2)
        else:
            self.axe.set_visible(True)#display error message panel
        plt.draw()
            
if __name__ == '__main__':
    main()
