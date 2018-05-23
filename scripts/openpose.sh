#! /bin/bash
cd /openpose-master
./build/examples/openpose/openpose.bin --hand --image_dir $1 --net_resolution 112x112 --write_keypoint_json $2 --no_display
#echo $1 $2
