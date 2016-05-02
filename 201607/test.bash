#!/bin/bash -xv

rostopic pub /switch_motors std_msgs/Bool True --once &
sleep 1

rostopic pub /motor_raw std_msgs/Int32MultiArray "layout:
  dim:
  - label: ''
    size: 0
    stride: 0
  data_offset: 0
data: [100,100]" --once

rostopic pub /motor_raw std_msgs/Int32MultiArray "layout:
  dim:
  - label: ''
    size: 0
    stride: 0
  data_offset: 0
data: [0,0]" --once

rostopic pub /switch_motors std_msgs/Bool False --once &
