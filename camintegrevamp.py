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

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
    camera = cv2.VideoCapture(0)
    time.sleep(0.25)

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

        # compute the bounding box for the contour, draw it on the frame,
        # and update the text
        (x, y, w, h) = cv2.boundingRect(c)
        # What does this do. Why don't I annotate code when I write it?
        # if y != h:
        #     if x != w:
        #         cv2.imwrite("frame%d.jpg" % count, frame[x:x+w,y:y+h])
        #         print('written')
        #         count += 1
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        rectsize = (abs(w - x) * abs(h - y))
        # rectloc =

        text = "I see you!"
        # This takes screenshots of every frame of video
        # cv2.imwrite("frame%d.jpg" % count, frame)
        rectnumber += 1
        print "Rectangle " + str(rectnumber), str(rectsize) + " pixels"
    # draw the text and timestamp on the frame
    print "number of rectangles: " + str(rectnumber)

    cv2.putText(frame, "Hello, {}".format(text), (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)

    # show the frame and record if the user presses a key
    cv2.imshow("Threshold", thresh)
    cv2.imshow("Camera Feed", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key is pressed, break from the loop
    if key == ord("q"):
        break
    framenum += 1
    rectnumber = 0

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()