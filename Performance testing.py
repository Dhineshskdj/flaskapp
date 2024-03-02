import cv2
import pickle
import cvzone
import numpy as np

# Set up width and height for parking slots
width, height = 107, 48

def test_user_interaction():
    # Define the mouse click event function
    def mouseClick(events, x, y, flags, params):
        if events == cv2.EVENT_LBUTTONDOWN:
            posList.append((x, y))
        if events == cv2.EVENT_RBUTTONDOWN:
            for i, pos in enumerate(posList):
                x1, y1 = pos
                if x1 < x < x1 + width and y1 < y < y1 + height:
                    posList.pop(i)

        with open('parkingSlotPosition', 'wb') as f:
            pickle.dump(posList, f)

    # Load initial positions or create a new list
    try:
        with open('parkingSlotPosition', 'rb') as f:
            posList = pickle.load(f)
    except:
        posList = []

    # Set up the window and mouse callback
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", mouseClick)

    while True:
        img = cv2.imread('carParkImg.png')
        for pos in posList:
            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()

def test_visualization():
    # Load the saved positions
    with open('parkingSlotPosition', 'rb') as f:
        posList = pickle.load(f)

    # Load the image
    img = cv2.imread('carParkImg.png')

    # Draw rectangles for parking slots
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)

    # Display the image
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def test_storage():
    # Load the saved positions
    with open('parkingSlotPosition', 'rb') as f:
        posList = pickle.load(f)

    # Print the loaded positions
    print("Loaded Positions:")
    print(posList)

def test_parking_space_detection():
    # Load the saved positions
    with open('parkingSlotPosition', 'rb') as f:
        posList = pickle.load(f)

    # Load the video feed
    cap = cv2.VideoCapture('carParkingInput.mp4')

    # Define the checkParkingSpace function
    def checkParkingSpace(imgPro):
        spaceCounter = 0

        for pos in posList:
            x, y = pos

            imgCrop = imgPro[y:y + height, x:x + width]
            count = cv2.countNonZero(imgCrop)

            if count < 900:
                color = (0, 255, 0)
                thickness = 5
                spaceCounter += 1
            else:
                color = (0, 0, 255)
                thickness = 2

            cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
            cvzone.putTextRect(img, str(count), (x, y + height - 3), scale=1,
                               thickness=2, offset=0, colorR=color)
        cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                           thickness=5, offset=20, colorR=(200, 0, 0))

# Call the functions
test_user_interaction()
test_visualization()
test_storage()
test_parking_space_detection()

