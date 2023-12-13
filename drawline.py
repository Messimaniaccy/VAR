import numpy as np
import cv2 as cv
import time

pts = []

def compute_intersection(line1,line2):
    x1,y1,x2,y2 = line1
    x3,y3,x4,y4 = line2
    slope1 = (y2-y1)/(x2-x1) if x2 != x1 else np.inf
    slope2 = (y4-y3)/(x4-x3) if x4 != x3 else np.inf
    if np.isinf(slope1) and np.isinf(slope2):
        return None
    if np.isinf(slope1):
        x = x1
        y = slope2*(x-x3)+y3
    elif np.isinf(slope2):
        x = x3
        y = slope1*(x-x1)+y1
    else:
        x = (slope1*x1-y1-slope2*x3+y3)/(slope1-slope2)
        y = slope1*(x-x1)+y1
    return (x,y)

def operation(event, x, y, flag, param):
    global pts,frame
    if event == cv.EVENT_LBUTTONDOWN:
        if len(pts) < 8:
            pts.append([x,y])
            cv.circle(frame,(x,y),5,(0,0,255),-1)
        else:
            print("You have already selected 8 points and the boundary of the field has been drawn!")
    elif event == cv.EVENT_RBUTTONDOWN:
        cv.circle(frame,(x,y),3,(0,0,255),-1)
        line1 = (pts[2][0],pts[2][1],pts[3][0],pts[3][1])
        line2 = (pts[6][0],pts[6][1],pts[7][0],pts[7][1])
        point1 = compute_intersection(line1,line2)
        line3 = (x,y,point1[0],point1[1])
        line4 = (pts[0][0],pts[0][1],pts[1][0],pts[1][1])
        line5 = (pts[4][0],pts[4][1],pts[5][0],pts[5][1])
        point2 = compute_intersection(line3,line4)
        point3 = compute_intersection(line3,line5)
        point2 = (int(point2[0]),int(point2[1]))
        point3 = (int(point3[0]),int(point3[1]))
        cv.line(frame,point2,point3,(255,0,0),thickness=2)
    elif event == cv.EVENT_MBUTTONDOWN:
        cv.circle(frame,(x,y),3,(0,0,255),-1)
        line1 = (pts[2][0],pts[2][1],pts[3][0],pts[3][1])
        line2 = (pts[6][0],pts[6][1],pts[7][0],pts[7][1])
        point1 = compute_intersection(line1,line2)
        line3 = (x,y,point1[0],point1[1])
        line4 = (pts[0][0],pts[0][1],pts[1][0],pts[1][1])
        line5 = (pts[4][0],pts[4][1],pts[5][0],pts[5][1])
        point2 = compute_intersection(line3,line4)
        point3 = compute_intersection(line3,line5)
        point2 = (int(point2[0]),int(point2[1]))
        point3 = (int(point3[0]),int(point3[1]))
        cv.line(frame,point2,point3,(0,255,0),thickness=2)
    cv.imshow("Detection",frame)
    
def detect(filename):
    global frame,pts
    frame = cv.imread(filename)
    cv.namedWindow("Detection")
    cv.setMouseCallback("Detection",operation)
    cv.imshow("Detection",frame)
    pts.clear()
    cv.waitKey(0)
    cv.destroyAllWindows()