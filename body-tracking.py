import cv2
import mediapipe as mp
import time

# Get camera
cap = cv2.VideoCapture(1)

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

# Calculate FPS
pTime = 0
cTime = 0
    
# Analysis loop
while True:
    success, imgRaw=cap.read()
    # Flip image 
    img = cv2.flip(imgRaw, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
            
    # Draw lines
    mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    
    # Draw FPS
    cTime = time.time()
    fps = int(1/(cTime-pTime))
    pTime = cTime

    cv2.putText(img, str(fps), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    # Refresh image
    cv2.imshow("Image", img)
    c=cv2.WaitKey(1)
    if c==27 or c == 1048603: #Break if user enters 'Esc'.
        break