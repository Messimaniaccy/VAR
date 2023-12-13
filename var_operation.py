'''
Virtual Assistant Referee(VAR)
Copyright 2023.12.13 Peking University
A VAR system with GUI
Usage: Input the recorded video file into the system and follow the instructions provided by         buttons and output prompts. It is also possible to control the Raspberry Pi camera via the    terminal in the Raspberry Pi environment.
Author: Chu ChenYuan
'''
import tkinter
import cv2 as cv
import PIL.Image,PIL.ImageTk
from functools import partial
import threading
import time
import imutils
import drawline
import football
import keyboard

stream = cv.VideoCapture("/Users/apple/Desktop/Virtual Assistant Referee/football_media/test_video/video3.mp4")
flag = True
pts = []

def play(speed):
	global flag
	print(f"You clicked on play. Speed is {speed}.")
	frame1 = stream.get(cv.CAP_PROP_POS_FRAMES)
	stream.set(cv.CAP_PROP_POS_FRAMES,frame1+speed)

	ret,frame = stream.read()
	if not ret:
		print("Video ended and thus quitting. Replay the program if you wish to see again.")
		exit()

	frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
	frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
	canvas.image = frame
	canvas.create_image(0,0,image=frame,anchor=tkinter.NW)

	if flag:
		canvas.create_text(140,40,fill="yellow",font="Times 26 bold",text="Decision Pending",anchor=tkinter.SW)
	flag = not flag

def pending(decision):
	img = cv.imread("/Users/apple/Desktop/Virtual Assistant Referee/football_media/VAR System/pending.png")
	frame = cv.cvtColor(img,cv.COLOR_BGR2RGB)
	frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
	frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
	canvas.image = frame
	canvas.create_image(0,0,image=frame,anchor=tkinter.NW)
	time.sleep(3)
	if decision == 'goal':
		decisionImage = "/Users/apple/Desktop/Virtual Assistant Referee/football_media/VAR System/goal.png"
	elif decision == 'not goal':
		decisionImage = "/Users/apple/Desktop/Virtual Assistant Referee/football_media/VAR System/no_goal.png"
	elif decision == 'offside':
		decisionImage = "/Users/apple/Desktop/Virtual Assistant Referee/football_media/VAR System/offside.png"
	else:
		decisionImage = "/Users/apple/Desktop/Virtual Assistant Referee/football_media/VAR System/not_offside.png"

	frame = cv.cvtColor(cv.imread(decisionImage),cv.COLOR_BGR2RGB)
	frame = imutils.resize(frame,width=SET_WIDTH,height=SET_HEIGHT)
	frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
	canvas.image = frame
	canvas.create_image(0,0,image=frame,anchor=tkinter.NW)

def save_frame():
	ret,frame = stream.read()
	if not ret:
		print("Error capturing frame.")
		return

	filename = f"/Users/apple/Desktop/Virtual Assistant Referee/captured_frame.png"
	cv.imwrite(filename,frame)
	print(f"Frame has been saved as {filename}")

	sub_window = tkinter.Tk()
	sub_window.title("VAR Operation")
	print("Please press the appropriate button to operate the algorithm")
	btn = tkinter.Button(sub_window,text="Detect Offside",width=50,command=lambda:drawline.detect(filename))
	btn.pack()
	btn = tkinter.Button(sub_window,text="Goal Check",width=50,command=lambda:football.goal_check(filename))
	btn.pack()

def goal():
	thread = threading.Thread(target=pending,args=("goal",))
	thread.daemon = 1
	thread.start()
	print("it is a goal")

def not_goal():
	thread = threading.Thread(target=pending,args=("not goal",))
	thread.daemon = 1
	thread.start()
	print("it is not a goal")

def offside():
	thread = threading.Thread(target=pending,args=("offside",))
	thread.daemon = 1
	thread.start()
	print("it is an offside")

def not_offside():
	thread = threading.Thread(target=pending,args=("not offside",))
	thread.daemon = 1
	thread.start()
	print("it is not an offside")

def exit_system():
	print("Exiting the system!")
	stream.release()
	cv.destroyAllWindows()
	exit()

def try_again():
	return

SET_WIDTH = 650
SET_HEIGHT = 368

window = tkinter.Tk()
window.title("Virtual Assistant Referee")
cv_img = cv.cvtColor(cv.imread("/Users/apple/Desktop/Virtual Assistant Referee/football_media/VAR System/welcome.png"),cv.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window,width=SET_WIDTH,height=SET_HEIGHT)
photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))
image_on_canvas = canvas.create_image(0,0,anchor=tkinter.NW,image=photo)
canvas.pack()

btn = tkinter.Button(window,text="<< Backward (fast)",width=50,command=partial(play,-25))
btn.pack()
btn = tkinter.Button(window,text="<< Backward (slow)",width=50,command=partial(play,-2))
btn.pack()
btn = tkinter.Button(window,text="Forward (fast) >>",width=50,command=partial(play,25))
btn.pack()
btn = tkinter.Button(window,text="Forward (slow) >>",width=50,command=partial(play,2))
btn.pack()
btn = tkinter.Button(window,text="Goal",width=50,command=goal)
btn.pack()
btn = tkinter.Button(window,text="No Goal",width=50,command=not_goal)
btn.pack()
btn = tkinter.Button(window,text="Offside",width=50,command=offside)
btn.pack()
btn = tkinter.Button(window,text="No Offside",width=50,command=not_offside)
btn.pack()
btn = tkinter.Button(window,text="Capture frame",width=50,command=save_frame)
btn.pack()
btn = tkinter.Button(window,text="Exit",width=50,command=exit_system)
btn.pack()
btn = tkinter.Button(window,text="Try Again",width=50,command=try_again)
btn.pack()

window.mainloop()
