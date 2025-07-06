# # There are mainly 5 steps to develop this project
# # The first step is to open up the video camera
# # Detect the Head
# # In step-3 we need to separate our index finger
# # In step-4 we have to move the mouse pointer using the index finger
# # In step 5 we are going to perform the click operation
# # When the index finger and the thumb come closer to each other then the event click is going to happen
# import cv2
# # To detect the hand movements
# import mediapipe as mp
# import pyautogui
# from PIL.ImageChops import screen
#
# cap=cv2.VideoCapture(0)
# hand_detector=mp.solutions.hands.Hands()
# drawing_utils=mp.solutions.drawing_utils
# screen_width,screen_height=pyautogui.size()
# index_y=0
# while(True):
#     _,frame=cap.read()
#     # flipCode zero indicates that it will flip on x-axis
#     # flipCode one indicates that it will flip on y-axis
#
#     frame=cv2.flip(frame,1)
#     frame_height,frame_width,_=frame.shape
#     rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
#     output=hand_detector.process(rgb_frame)
#     hands=output.multi_hand_landmarks
#     if hands:
#         for hand in hands:
#             drawing_utils.draw_landmarks(frame,hand)
#             landmarks=hand.landmark
#             for id,landmark in enumerate(landmarks):
#                 x=int(landmark.x*frame_width)
#                 y=int(landmark.y*frame_height)
#                 # print(x,y)
#                 if id==8:
#                     cv2.circle(img=frame,center=(x,y),radius=10,color=(0,255,255))
#                     index_x=(screen_width/frame_width)*x
#                     index_y = (screen_height / frame_height) * y
#
#                     pyautogui.moveTo(index_x,index_y)
#                 if id==4:
#                     cv2.circle(img=frame,center=(x,y),radius=10,color=(0,255,255))
#                     thumb_x=(screen_width/frame_width)*x
#                     thumb_y = (screen_height / frame_height) * y
#                     print(abs(index_y-thumb_y))
#                     if abs(index_y-thumb_y)<20:
#                         pyautogui.click()
#                         pyautogui.sleep(1)
#
#
#     cv2.imshow('Virtual Mouse',frame)
#     cv2.waitKey(1)
#


import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()
index_y = 0

while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark

            # Initialize coordinates
            index_finger = (0, 0)
            thumb = (0, 0)
            middle_finger = (0, 0)

            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                if id == 8:  # Index Finger Tip
                    index_finger = (x, y)
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y
                    pyautogui.moveTo(index_x, index_y)
                    cv2.circle(frame, center=(x, y), radius=10, color=(0, 255, 255))

                if id == 4:  # Thumb Tip
                    thumb = (x, y)
                    cv2.circle(frame, center=(x, y), radius=10, color=(0, 255, 255))

                if id == 12:  # Middle Finger Tip
                    middle_finger = (x, y)
                    cv2.circle(frame, center=(x, y), radius=10, color=(255, 0, 255))

            # Click Condition: Thumb and Index close
            if abs(index_finger[1] - thumb[1]) < 20:
                pyautogui.click()
                pyautogui.sleep(1)

            # Scroll Condition
            scroll_distance = middle_finger[1] - index_finger[1]

            if abs(scroll_distance) < 20:
                # Fingers close — scroll down
                pyautogui.scroll(-10)
            elif abs(scroll_distance) > 40:
                # Fingers apart — scroll up
                pyautogui.scroll(10)

    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
