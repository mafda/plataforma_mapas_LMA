#! /bin/bash

./vilma_detection_camera_scan.py > log/vilma_detection_camera_scan.log 2>&1 &
./vilma_compass.py > log/vilma_compass.log 2>&1 &
./vilma_position_vision_system.py > log/vilma_position_vision_system.log 2>&1 &

./vilma_velocity.py > log/vilma_velocity.log 2>&1 &
./vilma_all_sensor_data.py > log/vilma_all_sensor_data.log 2>&1 &

input=""
while [ ! "$input" == "q" ]; do
	read input
done

killall python

