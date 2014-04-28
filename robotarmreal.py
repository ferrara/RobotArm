from matplotlib.widgets import Slider, Button
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import time

# has two properties: length (l), and angle (a). Angle is relative to world, not parent bone.
class seg:
    def __init__(self, length, angle):
        self.l = length
        self.a = np.radians(angle) ## this is the actual angle, not relative. stored internally in rads


fig = plt.figure("CS 4TE3 Robot Simulator")
ax = plt.axes([0.05, 0.2, 0.90, .75],xlim=200,ylim=200)
ax.axis([0,200,0,200])
plt.ion()

temp = plt.axes([0.0, 0.0, 0.01, 0.01])
#but = Button(butval, '')
#but.on_clicked(move_click)


#plt.show()

        
basePos = [0,0] ## the static initial position (start point of first segment)
goalPos = [100, 100]
segments = [seg(80, 60), seg(100,60), seg(60, 60)]
nSegs = len(segments)



def draw(x,y):
           
    ax.cla() #clear current axis
    ax.plot(x,y,'o-', markersize=20, markerfacecolor="red", linewidth = 8, color="black")
    ax.plot(x,y,'o-', markersize=4, markerfacecolor="blue", linewidth = 1, color="silver")
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    #ax.relim()
    #ax.autoscale_view()
    
    plt.draw()
    
        

    # returns the segment's end point position in world coords. Ask for
    # a segment one lower to get the base point of the segment.
def getSegPos(segNum):
    pos = basePos[:]

    for i in range(segNum):
        pos[0] += segments[i].l * np.cos(segments[i].a)
        pos[1] += segments[i].l * np.sin(segments[1].a)
    return pos

# returns the current position of the tip of the robot arm.
# just a simple wrapper function
def getHeadPos():
    return getSegPos(nSegs) # this is technically outside the range of the segment list, but it works

# returns the displacement between two points (a - b)
def dist(a, b):
    s = list()
    for i in range(len(a)):
        s.append(a[i] - b[i])
    return s

# returns the distance between two points (as length)
def absDist(a, b):
    s = list()
    for i in range(len(a)):
        s.append(np.square(a[i] - b[i])) ## s[i]=(a.x - b.x)^2

    return np.sqrt(sum(s)) # sqrt((a.x - b.x)^2 + (a.y - b.y)^2)


# iterate through each segment, starting at the tip.
    # get angle between base of segment and current head pos,
    # and base of segment and target pos.
    
    # use rearranged sine, cosine laws to get angle between
    # the two vectors.

    # add this angle to your current angle (use sine law to
    # determine if angle is positive or negative)
def ccd():
    xs = [None]*4
    ys = [None]*4
    goalRadi = 10 # how close to the goal we need to get
    currentPos= getHeadPos() # current position of the tip
    print ("curr Pos: ", currentPos)
    print ("goal Pos: ", goalPos)
    iter = 0
    while(absDist(currentPos, goalPos) > goalRadi): # keep trying until close enough (or error)
        print ("iterations: ", iter)
        for i in reversed(range(nSegs)): #adjust each segment, starting at the tip

            currentPos= getHeadPos() # current position of the tip
            segPos = getSegPos(i) # position of the base of the current segment
            print ("segment ", i+1, " is at ", segPos)
            
            l2c = dist(currentPos, segPos) # line segment from current tip position to segment base position
            l2g = dist(goalPos, segPos) # line segment from goal position to segment base position
            absl2c = absDist(currentPos, segPos) # magnitude of segmnent
            absl2g = absDist(goalPos, segPos) # "
            
            # deltaTheta = arcsin( (a.x*b.y - a.y*b.x)/(abs(a) * abs(b)) )
            # for getting the direction of rotation
            sign_dAng = np.sign(np.arcsin((l2c[0]*l2g[1] - l2c[1]*l2g[0]) / (absl2c * absl2g)))
            
            # deltaTheta = arccos( (a.x*b.x + a.y*b.y) / abs(a) * abs(b)) )
            # for getting the magnitude of the rotation
            magn_dAng = np.arccos((l2c[0]*l2g[0] + l2c[1]*l2g[1]) / (absl2c * absl2g))
            
            dAng = sign_dAng * magn_dAng
            segments[i].a += sign_dAng * magn_dAng #update angle of the segment
            xs[i] = segPos[0]
            ys[i] = segPos[1]
            xs[3] = currentPos[0]
            ys[3] = currentPos[1]
            #draw(xs,ys)
            #time.sleep(2)
            
        
        draw(xs,ys)
        time.sleep(2)
        iter+=1
        
        print ("current arm head position: ", getHeadPos())
        
        if (iter > 100):
            print ("Error: could not reach point")
            break
        
    print ("position ", currentPos, " within accepted range of goal")
    return "lol"

def main():
    totalArmLength=0
    for seg in segments:
        totalArmLength += seg.l
    if (totalArmLength * 0.9 > absDist(goalPos, basePos)):
        ccd()
    else:
        print ("Error: goal point too far away")
        
if __name__ == '__main__':
    main()
                    
    
