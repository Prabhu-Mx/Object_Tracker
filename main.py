# Importing Libraries 
import cv2
from imutils.video import FPS

#Setting up video input
vs = cv2.VideoCapture('') #<<-- Enter your path of input video file 

#Get input video file width & height
width = int(vs.get(3))
height = int(vs.get(4))


#Initializing a tracker.
tracker = cv2.TrackerCSRT_create() # to read more about opencv trackers, please check this out https://docs.opencv.org/3.4/d2/d0a/tutorial_introduction_to_tracker.html

initBB = None
fps = None


fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter('pk0_traffic_output.mp4', fourcc, 35.0, (width, height))

while True:
    ret, frame = vs.read()
    print('Frame size-', frame.shape[:2])
    # check to see if we are currently tracking an object
    if initBB is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)
        print('sucess -', success)
        # check to see if the tracking was a success
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h),
                          (0, 255, 0), 2)
        # update the FPS counter
        fps.update()
        fps.stop()

        info = [
            ("Tracker", tracker),
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]
        # loop over the info tuples and draw them on our frame
    
        for (i, (k, v)) in enumerate(info):
            print("while loop")
            text = "{}: {}".format(k, v)
            print (text)
            cv2.putText(frame, text, (10, height - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    #Writing a output frames
    output.write(frame)
    cv2.imshow("Object_Tracker", frame)

    if cv2.waitKey(1) == ord("s"):
    # select the bounding box of the object we want to track (make
    # sure you press ENTER or SPACE after selecting the ROI)
        initBB = cv2.selectROI("Frame", frame, fromCenter=False,
                           showCrosshair=True)
        print(initBB)
    # start OpenCV object tracker using the supplied bounding box
        # coordinates, then start the FPS throughput estimator as well
        tracker.init(frame, initBB)
        fps = FPS().start()
    elif cv2.waitKey(1) == ord('q'):
        break

output.release()
vs.release()
cv2.destroyAllWindows()
