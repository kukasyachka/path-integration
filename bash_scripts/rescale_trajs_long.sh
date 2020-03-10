TRAJF=../results/trajectories/prepost_long
ls $TRAJF | parallel python ../scale_trajectory.py $TRAJF/{}

