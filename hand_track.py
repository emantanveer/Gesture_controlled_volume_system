import cv2
import mediapipe as mp
import time 

class hand_detector():
    def __init__(self, mode=False, max_hands=2, detectconf=0.5, trackconf=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.detectconf = detectconf
        self.trackconf = trackconf
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detectconf,
            min_tracking_confidence=self.trackconf
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None  # Initialize self.results to None

    def find_hands(self, frame, draw=True):
        frame_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(frame_RGB)  # Save the results to self.results

        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def find_position(self, frame, handno=0, draw=True):
        lmlist = []
        if self.results and self.results.multi_hand_landmarks:
            myhand = self.results.multi_hand_landmarks[handno]
            for id, lm in enumerate(myhand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # Append landmark data to the list
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(frame, (cx, cy), 5, (200, 162, 200), cv2.FILLED)
        return lmlist


def main():
    ptime = 0
    ctime = 0
    cap = cv2.VideoCapture(0)
    detector = hand_detector()
    while True:
        success, frame = cap.read()
        frame = detector.find_hands(frame)
        lmlist = detector.find_position(frame)
        if len(lmlist) != 0:
            print(lmlist[4])  # Print landmark 4 (e.g., thumb tip)

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (200, 162, 200), 3)
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
