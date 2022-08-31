import cv2
import mediapipe as mp
import time

def drawLines (img, points):
    if len(points) <= 1:
        return
    prev = points[0]
    for i in range(1,len(points)-1):
        cv2.line(img, prev, points[i], (255, 0, 255), 2)
        prev=points[i]


# First cammera
cap = cv2.VideoCapture(1)

mpHands = mp.solutions.pose
hands = mpHands.Pose()
mpDraw = mp.solutions.drawing_utils

# Calculate FPS
pTime = 0
cTime = 0

# Set up line drawing
cx_prev      = -1
cy_prev      = -1
points       = []
MAX_LEN      = 150
INDEX_FINGER = 8
    
# Analysis loop
while True:
    success, imgRaw=cap.read()
    # Flip image 
    img = cv2.flip(imgRaw, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)        
            
    # Draw lines
    mpDraw.draw_landmarks(img, results.pose_landmarks, mpHands.POSE_CONNECTIONS)
    
    # Draw FPS
    cTime = time.time()
    fps = int(1/(cTime-pTime))
    pTime = cTime

    cv2.putText(img, str(fps), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    # Refresh image
    cv2.imshow("Image", img)
    cv2.waitKey(1)