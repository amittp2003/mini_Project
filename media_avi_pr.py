import cv2 
import mediapipe as mp
import pyautogui
import time

def count_fingers(lst):
    
    # 'cnt' will track the how many fingers has been raised.
    cnt = 0

    thresh = (lst.landmark[0].y*100 - lst.landmark[9].y*100)/2
    
    # if forefinger(5-8) up 
    if (lst.landmark[5].y*100 - lst.landmark[8].y*100) > thresh:
        cnt += 1

    # if middle finger(9-12) up
    if (lst.landmark[9].y*100 - lst.landmark[12].y*100) > thresh:
        cnt += 1

    # if ring finger(13-16) up
    if (lst.landmark[13].y*100 - lst.landmark[16].y*100) > thresh:
        cnt += 1

    # if pinky finger(17-20) up
    if (lst.landmark[17].y*100 - lst.landmark[20].y*100) > thresh:
        cnt += 1
        
    # if thumb finger(5-4) up
    if (lst.landmark[5].x*100 - lst.landmark[4].x*100) > 6:
        cnt += 1

    return cnt 


#This will return video from the first webcam('0':default webcam) on your computer.
cap = cv2.VideoCapture(0)

# Initializing the drawing utils for drawing the hand landmarks on image.
drawing = mp.solutions.drawing_utils

hands = mp.solutions.hands

# how many hands you want detect in the frame.
hand_obj = hands.Hands(max_num_hands=1)

start_init = False 
prev = -1
cnt = 0

while True:
    end_time = time.time()
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

    # It will return the list of detected hands in the frame.
    if res.multi_hand_landmarks:

        # It will return the '0'th element in the list. 
        hand_keyPoints = res.multi_hand_landmarks[0]

        cnt = count_fingers(hand_keyPoints)

        if not(prev==cnt):
            # start time has not yet been initialised.
            if not(start_init):             
                start_time = time.time()
                start_init = True
                
             # 0.2 seconds give to user to how many fingers users wants to raised. 
            elif (end_time-start_time) > 0.2:
                
                 # 1 finger up == Forward.
                if (cnt == 1):
                    pyautogui.press("right")
                    
                 # 2 finger up == Backward.
                elif (cnt == 2):
                    pyautogui.press("left")
                    
                 # 3 finger up == Volume up/upward.
                elif (cnt == 3):
                    pyautogui.press("up")

                 # 4 finger up == Volume down/downward.
                elif (cnt == 4):
                    pyautogui.press("down")
                    
                 # 5 finger up == Play/Pause.
                elif (cnt == 5):
                    pyautogui.press("space")

                prev = cnt
                start_init = False

        drawing.draw_landmarks(frm, hand_keyPoints, hands.HAND_CONNECTIONS)

    cv2.putText(frm, "your finger input is: " + str(cnt), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
   
   
     # It will show output window to user. 
    cv2.imshow("window", frm)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        cap.release()
        break