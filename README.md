# OpenPose-Gesture-Recognition

In this project we made a hand gesture classifier, to classify the videos from the [20bn jester dataset](https://20bn.com/datasets/jester)

Instead of making a classifier from the ground up, we decided to use the [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose/) posture recognition framework from Carnegie Mellon University's Perceptual Computing Lab for representation. Using both the body and hand models, OpenPose allowed us to extract body- and hand pose keypoints from videos or images.

We then trained a long-short term memory recurrent neural network classifier on the sequence of keypoints extracted from each frame of the videos.

Our working pipeline worked as follows:
1. Parse as many videos as we could using OpenPose
2. Some data preprocessing, since not every video was succesfully parsed
3. Train the LSTM classifier

# Parsing of videos

Parsing is done using `run_openpose.py`. Here we input a video directory, which contains all frames as images, and run a subprocess that calls the actual openpose command. See the  `scripts/openpose.sh` file for the flags we have used. Note that we use a [OpenPose Docker](https://michaelsobrepera.com/guides/openposeaws.html), so the flags might be a bit different than in the newer versions. OpenPose outputs a directory of json files (one for each frame). After this we combine the jsons into one big json file.  

# Data Preprocessing

OpenPose was unfortunately unable to find people and extract their pose keypoints from a few videos (these were often cases that would be challenging for humans as well). We decided to prune the videos to make it easier for our classifier. Nex, we transformed the successful json outputs into a numpy array. See the notebook `RNN/Data Preprocessing.ipynb` for the criterion and transforming of the json files. In our case we eventually had $17054$ samples in our dataset. 

# Training the Classifier

The architecture of the LSTM RNN is based on [guillaume-chevalier's](https://github.com/guillaume-chevalier/LSTM-Human-Activity-Recognition). We also save performance summaries and the best performing models. See `RNN/Our Classifier.ipynb` for our implementation.

For training of the classifier, we randomly split our data into a training set of $14000$ and a test set of $3054$.


# Results

Our classifier had a test accuracy of around $50\%$. Note that this classifier was trained on a random sample consisting of only $10\%$ of the total 20bn jester training dataset - we believe that a higher accuracy could be achieved with more data. 
