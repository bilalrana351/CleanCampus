import cv2
from ultralytics import YOLO
import Paths
from Tracker import Tracker
import os
import requests
from PIL import Image
import io
import torch

Mpath = f"{Paths.MODEL_PATH}"

vPath = f"{Paths.VIDEO_PATH}"

appImageUploadUrl = f"{Paths.SERVER_URL_UPLOAD_ROUTE}"

# Load the YOLOv8 model
model = YOLO(model = Mpath)

# This wil be the approximated inference time of the model, you may change it based on your requirements
inference_time = 80.0

# This will be the average time of each frame
frame_time = 1000.0/60.0

# This will be the number of frames that will be skipped
skip_frames = int(inference_time/frame_time)

print(skip_frames)

# This will be the videoCapture instance of cv2
cap = cv2.VideoCapture(vPath)

# This will be the variable that will keep track of the fact whether the cuda is available or not, to enable gpu or not
cuda = torch.cuda.is_available()

if cuda:
    deviceToUse = 0
    willUseHalf = True
else:
    deviceToUse = "cpu"
    willUseHalf = False

# # This will be the tracker object, that will contain all the information about different objects in the video
# # At first we will give it an empty constructor, as it has not received any data till now
tracker = Tracker()

# This will be the total number of frames
frameNo = 0

litterBugImage = None

litterName = ""

# Loop through the video frames
while cap.isOpened():

    # Read a frame from the video
    success, frame = cap.read()

    if success:
        if (frameNo % skip_frames == 0 and frameNo >= 0):

            # Run YOLOv8 tracking on the frame, persisting tracks between frames
            results = model.track(frame, persist=True, imgsz = 1280, conf = 0.001, device = deviceToUse, iou = 0.3, rect = True, half = willUseHalf)

            # This will be the list of the bounding boxes of the detected objects
            # Should make it normalized
            boxes = results[0].boxes.xywhn.cpu().tolist()

            try:
                track_ids = results[0].boxes.id.int().cpu().tolist()

            # In case no track_ids have been defined we will initialize an empty list
            except AttributeError:
                track_ids = []

            # This will be the list of the classes of the detected objects
            classes = results[0].boxes.cls.cpu().tolist()


            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # This will update the id of the tracker
            currentState = tracker.update(classes,track_ids,boxes)

            if (currentState[0] == True):
                personBox = currentState[1]
                litterName = currentState[2]

                litterBugImage = frame
                break
            else:
                annotated_frame = cv2.resize(annotated_frame, (1200,1200))

                # Display the annotated frame
                cv2.imshow("Tracking", annotated_frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            
        frameNo += 1
        print(frameNo)
    else:
        # Break the loop if the end of the video is reached
        break

if (litterName == ""):
    pass

else:
    litterBugImage_pil = Image.fromarray(cv2.cvtColor(litterBugImage, cv2.COLOR_BGR2RGB))

    litterBugImage_pil.save("LitterBug.jpg")

    byteArrayImg = io.BytesIO()

    litterBugImage_pil.save(byteArrayImg,format="jpeg")

    requests.post(appImageUploadUrl, files = {"imageFile" : open("LitterBug.jpg","rb")}, data = {"fileName" : "can"})

# Release the video capture object and close the display window, in case all the frames have been opened
cap.release()
cv2.destroyAllWindows()