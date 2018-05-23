scrdir=./train/
outdir=./recog_test
N=50

for i in $( ls $scrdir | head -n $N ); do
	cp $scrdir/$i $outdir; done
