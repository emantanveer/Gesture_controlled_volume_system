import cv2
import time
import numpy as np
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import hand_track as ht  # Ensure this module exists and is correctly implemented

# Webcam dimensions
wcam, hcam = 640, 480

# Setup webcam
cap = cv2.VideoCapture(0)
cap.set(3, wcam)  # Set width
cap.set(4, hcam)  # Set height
ptime = 0

# Initialize hand detector
detector = ht.hand_detector(detectconf=0.7)

# Audio control setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Volume range
vol_range = volume.GetVolumeRange()  # (-65.25, 0.0, 0.03125)
min_vol = vol_range[0]
max_vol = vol_range[1]

# Volume variables
vol = 0
volbar = 400

while True:
    success, frame = cap.read()
    if not success:
        break

    # Resize frame (optional, not required if dimensions are already set)
    frame = cv2.resize(frame, (640, 480))

    # Detect hands and landmarks
    frame = detector.find_hands(frame)
    lmlist = detector.find_position(frame, draw=False)

    if len(lmlist) != 0:
        # Thumb tip coordinates
        x1, y1 = lmlist[4][1], lmlist[4][2]
        # Index finger tip coordinates
        x2, y2 = lmlist[8][1], lmlist[8][2]

        # Calculate center point
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Visualize points and line
        cv2.circle(frame, (x1, y1), 5, (200, 162, 200), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 5, (200, 162, 200), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (200, 162, 200), 3)
        cv2.circle(frame, (cx, cy), 5, (200, 162, 200), cv2.FILLED)

        # Calculate distance
        length = math.hypot(x2 - x1, y2 - y1)

        # Map length to volume range
        vol = np.interp(length, [50, 300], [min_vol, max_vol])
        volbar = np.interp(length, [50, 300], [400, 150])

        # Set volume
        volume.SetMasterVolumeLevel(vol, None)

        # Visual cue for close proximity
        if length < 50:
            cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        # Volume bar visualization
        cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(frame, (50, int(volbar)), (85, 400), (0, 255, 0), cv2.FILLED)

    # Calculate and display FPS
    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(frame, f"FPS: {int(fps)}", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (200, 162, 200), 3)

    # Show frame
    cv2.imshow("Volume Control", frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()


# import cv2 
# import time 
# import numpy as np
# import hand_track as ht
# import math
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# ############################################
# wcam,hcam=640,480
# #########################################3

# cap=cv2.VideoCapture(0)
# cap.set(3,wcam)
# cap.set(4,hcam)
# ptime=0

# detector=ht.hand_detector(detectconf=0.7)


# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(
#     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = interface.QueryInterface(IAudioEndpointVolume)
# # volume.GetMute()
# # volume.GetMasterVolumeLevel()

# vol_range=volume.GetVolumeRange()
# min_vol=vol_range[0]
# max_vol=vol_range[1]
# vol=0
# volbar=400
# while True:
#     success,frame=cap.read()
#     frame=cv2.resize(640,480)
#     frame=detector.find_hands(frame)
#     lmlist=detector.find_position(frame,draw=False)
#     if len(lmlist)  !=0:
#     #   print(lmlist[4],lmlist[8])

#       x1,y1=lmlist[4][1],lmlist[4][2]
#       x2,y2=lmlist[8][1],lmlist[8][2]
#       cx,cy=(x1+x2)//2,(y1+y2)//2
#       cv2.circle(frame,(x1,y1),5,(200,162,200),cv2.FILLED)
#       cv2.circle(frame,(x2,y2),5,(200,162,200),cv2.FILLED)
#       cv2.line(frame,(x1,y1),(x2,y2),(200,162,200),3)
#       cv2.circle(frame,(cx,cy),5,(200,162,200),cv2.FILLED)
#       length=math.hypot(x2-x1,y2-y1)
#       #hand range 50-300, vol -65 to 0
#       vol=np.interp(length,[50,300],[min_vol,max_vol])
#       volbar=np.interp(length,[50,300],[400,150])
#       volume.SetMasterVolumeLevel(vol, None)

#       if length<50:
#          cv2.circle(frame,(cx,cy),5,(255,0,255),cv2.FILLED)
#       cv2.rectangle(frame,(50,150),(85,400),(0,255,0),3)
#       cv2.rectangle(frame,(50,int(volbar)),(85,400),(0,255,0),cv2.FILLED)




#     ctime = time.time()
#     fps = 1 / (ctime - ptime)
#     ptime = ctime
#     cv2.putText(frame, f"FPS:{int(fps)}", (10, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (200, 162, 200), 3)


#     cv2.imshow("frame",frame)
#     cv2.waitKey(1)