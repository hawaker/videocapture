# -*- coding: utf-8 -*-
import numpy as np
import cv2
import datetime
import os
from sys import argv


def makevideothumb(filename,number,span=3):
  print("%s|proc|%s"%(datetime.datetime.now().strftime('%m-%d %H:%M:%S'),filename))
  #load video
  cap = cv2.VideoCapture(filename)
  #get video width and height
  width=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  height=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  if number%span>0:
    row=int((number+span-1)/span)
  else:
    row=int(number/span)
  # create numpy array
  emptyimg = np.zeros((height * row, width * span, 3), np.uint8)
  #get the total frame of the video
  count=cap.get(cv2.CAP_PROP_FRAME_COUNT)
  h=w=0
  while(cap.isOpened()):
    for i in range(number):
      heights=height*h
      widths=width*w
      frame=1/number*i*count
      cap.set(cv2.CAP_PROP_POS_FRAMES ,frame)
      ret,frame=cap.read()
      time=datetime.datetime.utcfromtimestamp(cap.get(cv2.CAP_PROP_POS_MSEC)/1000).strftime('%H:%M:%S')
      cv2.putText(frame, time, (10,45),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
      emptyimg[heights:heights + height, widths:widths + width] = frame[0:height, 0:width]
      if (w==span-1):
        h += 1
        w = 0
      else:
        w += 1
      # save frame as image
      #cv2.imwrite("%d.jpg"%i,frame)
    break
  #cv2.putText(emptyimg, "author:hawaker", (50, 45), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)
  cv2.imencode('.jpg', emptyimg)[1].tofile("%s.jpg" % filename)
  cap.release()
  print("%s|done|%s.jpg" % (datetime.datetime.now().strftime('%m-%d %H:%M:%S'), filename))
  

def main():
  if len(argv)>1:
    serchdirs(" ".join(argv[1:]))
  else:
    serchdirs()
      

def serchdirs(dir="."):
  if os.path.isfile((dir)):
    if isvideofile(dir):
      makevideothumb(dir,24,4)
  else:
    dirs=os.listdir(dir);
    for i in dirs:
      nowpath="%s\\%s"%(dir,i)
      serchdirs(nowpath)

  
def isvideofile(pathname):
  videofile=['.mp4','.avi','.mkv']
  fileinfo=os.path.splitext(pathname)
  if len(fileinfo)>1:
    return fileinfo[1] in videofile
  return False
  
if __name__=="__main__":
  main()