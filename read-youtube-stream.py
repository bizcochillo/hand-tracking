#pip install pafy
#sudo pip install --upgrade youtube_dl
import cv2, pafy
import mediapipe as mp

url   = "https://www.youtube.com/watch?v=GHbKOr1wurI"
video = pafy.new(url)
best  = video.getbest(preftype="any")

#documentation: https://pypi.org/project/pafy/

capture = cv2.VideoCapture(best.url)

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

while True:
    check, frame = capture.read()
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
            
    # Draw lines
    mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
    

    cv2.imshow('frame',frame)
    c=cv2.WaitKey(1)
    if c==27 or c == 1048603: #Break if user enters 'Esc'.
        break


    
capture.release()
cv2.destroyAllWindows()
