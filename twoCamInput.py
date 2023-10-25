# this code is for the utilization of two camera input for better detection
import cv2
import pyautogui
from time import time
from math import hypot
import mediapipe as mp
import matplotlib.pyplot as plt

# Initialize mediapipe pose class.
mp_pose = mp.solutions.pose
# Setup the Pose function for videos.
pose_video = mp_pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.7,
                          min_tracking_confidence=0.7)

# Initialize mediapipe drawing class.
mp_drawing = mp.solutions.drawing_utils

# function for detecting the pose
def detectPose(image, pose, draw=False, display=False):
    # Create a copy of the input image.
    output_image = image.copy()

    # Convert the image from BGR into RGB format.
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Perform the Pose Detection.
    results = pose.process(imageRGB)

    # Check if any landmarks are detected and are specified to be drawn.
    if results.pose_landmarks and draw:

        # Draw Pose Landmarks on the output image.
        mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS,
                                  landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 255, 255),
                                                                               thickness=3, circle_radius=3),
                                  connection_drawing_spec=mp_drawing.DrawingSpec(color=(49, 125, 237),
                                                                                 thickness=2, circle_radius=2))

    # Check if the original input image and the resultant image are specified to be displayed.
    if display:

        # Display the original input image and the resultant image.
        plt.figure(figsize=[22, 22])
        plt.subplot(121)
        plt.imshow(image[:, :, ::-1])
        plt.title("Original Image")
        plt.axis('off')
        plt.subplot(122)
        plt.imshow(output_image[:, :, ::-1])
        plt.title("Output Image")
        plt.axis('off')

    # Otherwise
    else:

        # Return the output image and the results of pose landmarks detection.
        return output_image, results

#function to check left right
def checkLeftRight(image, results, draw=False, display=False):
    # Declare a variable to store the horizontal position (left, center, right) of the person.
    horizontal_position = None
    
    # Get the height and width of the image.
    height, width, _ = image.shape
    
    # Create a copy of the input image to write the horizontal position on.
    output_image = image.copy()
    
    # Retreive the x-coordinate of the left shoulder landmark.
    left_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x * width)

    # Retreive the x-corrdinate of the right shoulder landmark.
    right_x = int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x * width)
    
    # Check if the person is at left that is when both shoulder landmarks x-corrdinates
    # are less than or equal to the x-corrdinate of the center of the image.
    if (right_x <= width//2 and left_x <= width//2):
        
        # Set the person's position to left.
        horizontal_position = 'Left'

    # Check if the person is at right that is when both shoulder landmarks x-corrdinates
    # are greater than or equal to the x-corrdinate of the center of the image.
    elif (right_x >= width//2 and left_x >= width//2):
        
        # Set the person's position to right.
        horizontal_position = 'Right'
    
    # Check if the person is at center that is when right shoulder landmark x-corrdinate is greater than or equal to
    # and left shoulder landmark x-corrdinate is less than or equal to the x-corrdinate of the center of the image.
    elif (right_x >= width//2 and left_x <= width//2):
        
        # Set the person position in center
        horizontal_position = 'Center'
        
    # Check if the person's horizontal position and a line at the center of the image is specified to be drawn.
    if draw:

        # Write the horizontal position of the person on the image. 
        cv2.putText(output_image, horizontal_position, (5, height - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
        
        # Draw a line at the center of the image.
        cv2.line(output_image, (width//2, 0), (width//2, height), (255, 255, 255), 2)
        
    # Check if the output image is specified to be displayed.
    if display:

        # Display the output image.
        plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("Output Image");plt.axis('off');
    
    # Otherwise
    else:
    
        # Return the output image and the person's horizontal position.
        return output_image, horizontal_position

#taking the input
cap1 = cv2.VideoCapture(1)
cap2 = cv2.VideoCapture(0)
cap1.set(3,1280)
cap1.set(4,960)
cap2.set(3,1280)
cap2.set(4,960)
xpos = 1
cv2.namedWindow('Game',cv2.WINDOW_NORMAL)
time1 = 0
while cap1.isOpened() and cap2.isOpened():
    ok,frame = cap1.read()
    yes,frame1 = cap2.read()
    if not ok:
        continue
    if not yes:
        continue
    frame = cv2.flip(frame,1)
    frame1 = cv2.flip(frame1,1)
    frame_height, frame_width, _ = frame.shape
    frame_height, frame_width, _ = frame1.shape
    frame, results = detectPose(frame,pose_video, draw=True)
    if results.pose_landmarks:
        frame, horizontal_position = checkLeftRight(frame, results, draw=True)
        if (horizontal_position=='Left'):
            if(xposleft==False):
                pyautogui.keyDown('left')
                # print("kdl")
                xposleft = True
            else:
                # print("1")
                continue
            # print(x_pos_index)
        if (horizontal_position=='Center'):
            pyautogui.keyUp('left')
            # print("ku")
            xposleft = False
            pyautogui.keyUp('right')
            xposright = False
            # print(x_pos_index)
        if (horizontal_position=='Right'):
            if(xposright==False):
                pyautogui.keyDown('right')
                # print("kdr")
                xposright = True
            else:
                # print("2")
                continue
            # print("right"))
    frame1, res = detectPose(frame1,pose_video, draw=True)
    if res.pose_landmarks:
        frame1, horizontal_position = checkLeftRight(frame1, res, draw=True)
    time2 = time()
    if (time2-time1)>0:
        frames_per_second = 1.0 / (time2 - time1)
    time1 = time2
    cv2.imshow('The Game', frame1)
    k = cv2.waitKey(1) & 0xFF
    if(k == 27):
        break
cap1.release()
cv2.destroyAllWindows()



