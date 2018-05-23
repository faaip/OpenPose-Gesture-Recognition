scrdir=/home/ubuntu/20bn-datasets/20bn-jester-v1
outdir=/home/ubuntu/data/OpenPose-Gesture-Recognition/images
N=50

for i in $( ls $scrdir | head -n $N ); do
	cp -r $scrdir/$i $outdir; done
