# Muro
This is a repo for the object detection / obstacle avoidance scripts. We currenlty use the Sud Folder for our object detection. The entire folder must be on the turtle bot as the the test3.py script relies on the other two files.
There are other scripts here that can be extended for progamatic object detection however we circled back to using yolov8n.


To create the dataset for training I used fiftyone to filter COCO to the desired classes and made my own images of chairs and turtlebots and labeled them on roboflow, then concatenated the datasets.


For training once you pick an amount of epochs you are stuck with it because the learning optimizer is reset with each train in yolo8. So currently if you train for 250 epochs and see that it has not converged there is no way to train for another x epochs. The work around is to select a large number of epochs at the start and interrupt the training, which can be resumed using the resume=True flag in the !yolo mode=detect... line. This is a frequent problem on the Ultralytics docs discussion boards. This is something I would like to change manually when time permits. 


Do not attempt to train without gpu support, its pointless. https://www.youtube.com/watch?v=r7Am-ZGMef8 follow this for directions on how to set up cuda if you have a nvidia graphics card.

To train on google colab follow this https://www.youtube.com/watch?v=LNwODJXcvt4, though getting the dataset uploaded there would be very tricky.
