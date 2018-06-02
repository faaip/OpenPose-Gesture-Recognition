# OpenPose-Gesture-Recognition

In this project we made a classifier, to classify the videos from the [20bn jester dataset](https://20bn.com/datasets/jester)

Instead of making a classifier from the ground up, we decided to use the [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose/) posture recognition from Carnegie Mellon University's Perceptual Computing Lab.

This software allowed us to extract pose key points from images, this also contains a flag so that the hand model is included which we would need to classify the actual gestures.

Our working pipeline worked as follows:
1. Parse as many videos as we could using OpenPose
2. Some data preprocessing, since not every video was succesfully parsed
3. Train the classifier

# Parsing of video's

This part in centered around the `run_openpose.py`.
Here we get a video directory, which contains all the images and run a subprocess that calls the actual openpose command. See the  `scripts/openpose.sh` file to see what flags we have used. Note that we use a [OpenPose Docker](https://michaelsobrepera.com/guides/openposeaws.html) so the flags might be a bit differnt with the newer versions. In the end OpenPose output a directory of json files (one for each frame). After this we combine the jsons to une big json file.  

# Data Preprocessing

OpenPose was unfortunately not always succesful with parsing an images. This resulted in a some corrupt videos. We decided to prune the video's to make it easier for our classifier. In this step we transformed the allowed json video's to a numpy array. See the notebook `RNN/Data Preprocessing.ipynb` for the criterion and transforming of the json files. In our case we eventually had $17054$ samples in our dataset. 

# Training the Classifier

The architecture of the RNN is based on [guillaume-chevalier](https://github.com/guillaume-chevalier/LSTM-Human-Activity-Recognition). But besides this we also save summaries and best performing models. See `RNN/Our Classifier.ipynb` for our implementation.

For training of the classifier we took our dataset and randomly seperate it in a training set of $14000$ and a test set of $3054$.


# Results

We ended up with a classifier that had an accuracy off around $50\%$. But note that this classifier was trained on $10\%$ of the total dataset, our hope is that more data would result in a higher accuracy. 
