#! /bin/bash
cd /home/maxim/openpose/
./build/examples/openpose/openpose.bin --hand --image_dir $1 --net_resolution 112x112 --write_json $2 --display 0
#echo $1 $2
