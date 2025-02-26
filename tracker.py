# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 22:55:13 2025

@author: Bibun
"""
import cv2
import mediapipe as mp
import numpy as np
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1]-b[1],c[0]-b[0]) -np.arctan2(a[1]-b[1],a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360 - angle
    return angle
        

cap = cv2.VideoCapture(0)
lcounreps = 0
rcounreps = 0
lstage = None
rstage = None

with mp_pose.Pose(min_detection_confidence=0.5,min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
       ret, frame = cap.read()
    
       image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
       image.flags.writeable = False
    
       results = pose.process(image)
    
       image.flags.writeable = True
       image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
       
       try:
           landmarks = results.pose_landmarks.landmark
           
           #for left part
           left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
           left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
           left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
         
         # Calculate angle
           left_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
          
         # Visualize angle
           cv2.putText(image, str(left_angle), 
                        tuple(np.multiply(left_elbow, [640, 480]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                             )
           
           if left_angle > 160:
               lstage = "down"
           if left_angle < 30 and lstage == "down":
                   lstage = "up"
                   lcounreps +=1
                   print(lcounreps)
           
         # for right part
           right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
           right_elbow =  [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
           right_wrist =  [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
       
           right_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)
        
           cv2.putText(image,str(right_angle),
                    tuple(np.multiply(right_elbow,[640,480]).astype(int)),
                          cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,243,194),2,cv2.LINE_AA)
           
         
                   
           if right_angle > 160:
               rstage = "down"
           if right_angle < 30 and rstage == "down":
                   rstage = "up"
                   rcounreps +=1
                   print(rcounreps)
                   
       except:   
           pass
       
       cv2.rectangle(image, (0, 0), (300, 73), (245, 117, 16), -1)

# Left Reps
       cv2.putText(image, 'L_REPS', (10, 20), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
       cv2.putText(image, str(lcounreps), (10, 50), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

# Right Reps
       cv2.putText(image, 'R_REPS', (80, 20),  
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
       cv2.putText(image, str(rcounreps), (80, 50),  
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

# Left Stage
       cv2.putText(image, 'L_STAGE', (150, 20),  
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
       cv2.putText(image, str(lstage), (150, 50),  
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

# Right Stage
       cv2.putText(image, 'R_STAGE', (220, 20),  
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1, cv2.LINE_AA)
       cv2.putText(image, str(rstage), (220, 50),  
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)


    
       mp_drawing.draw_landmarks(image, results.pose_landmarks,mp_pose.POSE_CONNECTIONS,
                                 mp_drawing.DrawingSpec(color=(53, 20, 245),thickness=3,circle_radius=2),
                                 mp_drawing.DrawingSpec(color=(242, 200, 82),thickness=3,circle_radius=2))
       cv2.imshow('Track_It', image)
    
       if cv2.waitKey(10) & 0xFF == ord('q'):
          break
        
cap.release()
cv2.destroyAllWindows()

