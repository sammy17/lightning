import sys
import cv2
import numpy as np
import image
import time
#import matplotlib.pyplot as plt
#import matplotlib.image as mpimg

SCALE = 0.5
NOISE_CUTOFF = 5
BLUR_SIZE = 3

start = time.time()

def count_diff(img1, img2):
    small1 = cv2.resize(img1, (0,0), fx=SCALE, fy=SCALE)
    small2 = cv2.resize(img2, (0,0), fx=SCALE, fy=SCALE)
    diff = cv2.absdiff(small1, small2)
    diff = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
    frame_delta1 = cv2.threshold(diff, NOISE_CUTOFF, 255, 3)[1]
    #frame_delta1_color = cv2.cvtColor(frame_delta1, cv2.COLOR_GRAY2RGB)
    delta_count1 = cv2.countNonZero(frame_delta1)

    return delta_count1

filename = sys.argv[1]
treshold = float(sys.argv[2])
if not (treshold > 0 and treshold <100):
    print("Invalid threshold value -> threshold must be greater than 0 and less than 100\n")
    sys.exit()
video = cv2.VideoCapture(filename)

nframes = (int)(video.get(cv2.CAP_PROP_FRAME_COUNT))
width = (int)(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = (int)(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps= (int)(video.get(cv2.CAP_PROP_FPS))

frame_count = 0

print( "[i] Frame size: ", width, height)
print("[i] Total frames:", nframes)
print("[i] Fps:", fps)

treshold = treshold * width * height/100

fff = open(filename+".csv", 'w')

flag, frame0 = video.read()

strikes = 0

for f in range(nframes-1):
    flag, frame1 = video.read()
    diff1  = count_diff(frame0, frame1)
    name = filename+"_%06d.jpg" % f

    if diff1 > treshold:
        cv2.imwrite(name, frame1)
        strikes = strikes + 1

    text = str(f)+', '+str(diff1)
    fff.write(text  + '\n')
    fff.flush()
    frame0 = frame1

fff.close()
print( '[i] Strikes: ', strikes)
print( '[i] elapsed time:', time.time() - start)
