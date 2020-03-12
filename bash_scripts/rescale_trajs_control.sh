TRAJF=../results/trajectories/prepost_control
ls $TRAJF | parallel python ../scale_trajectory.py $TRAJF/{}

