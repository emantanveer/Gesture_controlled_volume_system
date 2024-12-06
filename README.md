# Gesture_controlled_volume_system
This project demonstrates a gesture-controlled volume control system using computer vision and hand-tracking techniques. It leverages Mediapipe for hand detection and tracking, and PyCaw for interacting with the system's audio volume.

**Features**

-**Hand Detection and Tracking:** Real-time detection and tracking of hands using Mediapipe.

-**Volume Control:** Adjust the system volume by varying the distance between the thumb and index finger.

-**Visual Feedback:** Displays landmarks, connections, and a volume bar to indicate current volume levels.

-**Real-Time Performance:** Achieves smooth performance with FPS displayed on the screen.

**Modules**

**1. Volume Control Module**

-Detects the distance between the thumb and index finger.

-Maps the distance to the system volume range using PyCaw.

-Displays real-time feedback, including a dynamic volume bar.

**2. Hand Tracking Module**

-Tracks hand landmarks using Mediapipe.

-Identifies positions of specific landmarks like the thumb and index finger.

-Visualizes hand connections and landmarks on the webcam feed.
