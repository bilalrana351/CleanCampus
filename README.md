# CleanCampus

Welcome to CleanCampus, an AI-Powered Solution to prevent littering.

## Problem

- Littering is a very serious problem, it can lead to an increase in global warming.
- Countries like the US spend an estimated 11.5 Billion Dollars on their efforts to clean litter.

## Solution

- We have trained a YOLOv8m model to detect a person and the litter they are throwing. If littering activity is detected, the face of the person is sent to a database, matched with an existing person's face, and then fined accordingly.
- ByteTrack algorithm is used to track the persons and the litter.

## Litter Classes

- Paper
- Cardboard
- Can
- Plastic

## Training Examples

- About 1500

## Technologies

- YOLOv8m Object Detection Model
- ByteTrack Tracking Algorithm
- MySQL for the Database
- `image_recognition` of Python for the computation of the face embeddings
- Tkinter for the application
- Flask for connecting the model to the Application

## Future

- The application paves and proposes promising ways to detect litterbugs; however, more real-world training datasets will be required to bring the model up to mark for real-world use cases.
- Making better UI and application for the admin, and adding additional features.
- Deploying the model on CCTV.

## Additional Notes

- If you have an NVIDIA-GPU enabled machine, make sure to install the CUDA library to enable GPU inference.
- Make sure to have `dlib` installed for the `image_recognition` library.
- Make sure that you are in the same directory as the script that is going to be executed, otherwise you might get a path error, for example, if you are executing the code for detection and tracking, make sure that you are in the directory DetectionAndTracking, according to your terminal.