# OpenPose-Gesture-Recognition

In this project we made a classifier, to classify the videos from the [20bn jester dataset](https://20bn.com/datasets/jester)

Instead of making a classifier from the ground up, we decided to use the [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose/) posture recognition from Carnegie Mellon University's Perceptual Computing Lab.

Our working pipeline worked as follows:
1. Parse as many videos as we could using OpenPose
2. Some data preprocessing, since not every video was succesfully parsed
3. Train the classifier

