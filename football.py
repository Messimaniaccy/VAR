import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO("models/yolov8x")
pts = []

def compute_line(event,x,y,flag,param):
	global pts,img,model,result
	if event == cv2.EVENT_LBUTTONDOWN:
		if len(pts) < 3:
			pts.append((x,y))
			cv2.circle(img,(x,y),2,(0,0,255),thickness=-1)
		else:
			print("You have determined the goal line!")
			slope = (pts[0][1]-pts[1][1])/(pts[0][0]-pts[1][0])
			intercept = pts[0][1] - pts[0][0]*slope
			A = np.array([pts[0][0],pts[0][1]])
			B = np.array([pts[1][0],pts[1][1]])
			C = np.array([pts[2][0],pts[2][1]])
			vector1 = B-A
			vector2 = C-A
			for result in results:
				for obj_xyxy,obj_cls in zip(result.boxes.xyxy,result.boxes.cls):
					obj_cls = int(obj_cls)
					if obj_cls == 32: # 32 is the ball's ID in YOLO
						x1 = obj_xyxy[0].item()
						y1 = obj_xyxy[1].item()
						x2 = obj_xyxy[2].item()
						y2 = obj_xyxy[3].item()
						print(x1,y1,x2,y2)
						ball_x = (x2+x1)/2
						ball_y = (y2+y1)/2
						ball_r = ((x2-x1)+(y2-y1))/4
						yhat = ball_x * slope + intercept
						cv2.circle(img,(int(ball_x),int(ball_y)),2,(0,0,255),thickness=-1)
						cv2.circle(img,(int(ball_x),int(yhat)),2,(0,255,0),thickness=-1)
						print (ball_y, yhat)
						if yhat > ball_y:
							goal = False
							print("No Goal!")
						else:
							distance = abs(slope*ball_x-ball_y+intercept)/(slope**2+1)**0.5
							print(distance, ball_r)
							if distance > ball_r:
								goal = True
								print("GOAAAAAAAAL~")
							else:
								goal = False
								print("No Goal!")
				cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
		cv2.imshow("Goal Check",img)
def goal_check(filename):
	global img,results,pts
	img = cv2.imread(filename)
	results = model.predict(source=img)
	cv2.namedWindow("Goal Check")
	cv2.setMouseCallback("Goal Check",compute_line)
	cv2.imshow("Goal Check",img)
	pts.clear()
	cv2.waitKey(0)
	cv2.destroyAllWindows()
