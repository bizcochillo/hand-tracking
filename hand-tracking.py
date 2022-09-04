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
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
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

    # Hand recogniziton 
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h,w,c=img.shape
                cx,cy=int(lm.x * w), int(lm.y * h)


                if id == INDEX_FINGER:
                    if cx_prev != -1:
                        points.append((cx, cy))
                        if len(points) > MAX_LEN:
                            del points[0]                        
                    
                    cv2.circle(img, (cx, cy), 6, (255, 0, 255), cv2.FILLED)
                    cx_prev = cx
                    cy_prev = cy
            
    # Draw lines
    drawLines(img, points)
    
    # Draw FPS
    cTime = time.time()
    fps = int(1/(cTime-pTime))
    pTime = cTime

    cv2.putText(img, str(fps), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    # Refresh image
    cv2.imshow("Image", img)
    c=cv2.waitKey(1)
    if c==27 or c == 1048603: #Break if user enters 'Esc'.
        break