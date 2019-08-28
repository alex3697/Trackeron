# Tracker
Here is the explanation of how the tracker works, in order to detect first and last time that the target appears.

## Introduction

Here we are going to see how this program works:
You will need to install the opencv library (the full version) to your virtual environment, to accomplish this you can try `pip install opencv-contrib-python` this could help. It is important to be sure that only one version of opencv is installed.
This program is designed to track a certain object through a video saying first and last time that the object appears in the video. 

## Structure

The program follows the next structure:
Starts with a main where all the inputs are introduced in the following way:
- -i → Tells the path of the txt if all the data is introduced with a txt.
- -f → Tells the input format of the time.
- -a → Tells the path where the video is.
- -k → Tells the time where the object is in the specified time.
- -b → Tells the position of the bounding box.
- -s → Changes the step size in which the video is analized, in default 10.


The main will always call two functions, the first one will transform the video in a list of frames and will call the other 4 times:

 1. The first time will go through all the frames, starting in the one we designed, in the desired step, until loosing the target object.
2. The second will get the frame before loosing the object from the previous function and will go over the frames with the same objective, but this time frame by frame.
3. This time it will repeat the first step but in the other side.
4. Will repeat the second step but this time following the third step.

In this way we will have the exact frames where the object appears and disappears.
It also includes a function in order to know if at certain time the object is detected, since in the program we consider that the object is lost if it is not found in 10 steps.

## Kernelized Correlation Filter (KCF)
The tracker used in this case is the KCF (Kernelized Correlation Filter), this tracker estimates an optimal filter that the filtration with the input image produces a desired response. The answer is typically a Gaussian shape centered at the target location.
The response of the filter is evaluated and the maximum gives the new position of the target.
This filter is updated successively with every frame in order the tracker adapts to moderate target changes.
The major advantage of this type of tracker is the computational efifciency, since all the computation can be performed in the Fourier domain.

