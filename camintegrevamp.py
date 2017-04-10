import argparse
import datetime
import imutils
import time
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())
# Initializing variables used for calculations
count = 0
rectnumber = 0
framenum = 1
rectlist = []
xlist = []
mn = 0
prevmn = 0

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    camera = cv2.VideoCapture("/Users/me/Documents/GitHub/lego-model/pieces on conveyor slow.mov")
    time.sleep(0.25)

# otherwise, we are reading from a video file
else:
    camera = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
    # grab the current frame and initialize the occupied/unoccupied
    # text
    (grabbed, frame) = camera.read()
    print "Frame number: "+str(framenum)
    text = "I'm Lonely :("

    # if the frame could not be grabbed, then we have reached the end
    # of the video
    if not grabbed:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # This is done to even out small variations in the photo. it basically is taking a 21/21 pixel section and evaluating it as one pixel
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue


    # compute the absolute difference between the current frame and
    # first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

    # dilate the thresholded image to fill in holes, then find contours
    # on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    # Below line is for cv2. In open cv 3 you need to give room to call three sources as showin in the second line below
    # (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    (_, cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # loop over the contours
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < args["min_area"]:
            continue

        # compute the bounding box for the contour
        (x, y, w, h) = cv2.boundingRect(c)
        # add this bounding box to rectlist
        rectlist.append([x, y, w, h])
        # Calculating rectangle size
        rectsize = (abs(w - x) * abs(h - y))

        text = "I see you!"
        # This takes screenshots of every frame of video
        # cv2.imwrite("frame%d.jpg" % count, frame)
        rectnumber += 1
        print "Rectangle " + str(rectnumber), str(rectsize) + " pixels"
    # draw the text and timestamp on the frame
    print "number of rectangles: " + str(rectnumber)
    print "list is: " + str(rectlist)

    # makes list of y values
    for r in rectlist:
        xlist.append(r[0])

    # defines largest y value when I did this with x values it picked the one that was highest
    if len(xlist) != 0:
        mn = min(xlist)
    # draw draw contour rectangles. the rightmost one should be a different color
    for r in rectlist:
        if r[0] == mn:
            # draws red rectangle on the rightmost(rectangle)
            cv2.rectangle(frame, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (0, 0, 255), 2)
            # if the right most rectangle has changed since the last frame take snapshot
            if mn - prevmn > 25:
                cv2.imwrite("rect%d.jpg" % count, frame[r[0]:r[0] + r[2], r[1]:r[1] + r[3]])
                count += 1
        else:
            cv2.rectangle(frame, (r[0], r[1]), (r[0] + r[2], r[1] + r[3]), (255, 0, 0), 2)

    #adding cosmetic texts
    cv2.putText(frame, "Hello, {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

    # prints minimum x value

    print mn


    # show the frame and record if the user presses a key
    cv2.imshow("Threshold", thresh)
    cv2.imshow("Camera Feed", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the loop
    if key == ord("q"):
        break
    framenum += 1
    rectnumber = 0
    rectlist = []
    xlist= []
    prevmn = mn

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()