#! /bin/bash

roscore > log/roscore.log 2>&1 &
rosrun gazebo_ros gazebo vilma_simulacao.world > log/gazebo.log 2>&1 &

input=""
while [ ! "$input" == "q" ]; do
	read input
done

killall gzclient
killall gzserver
killall roscore