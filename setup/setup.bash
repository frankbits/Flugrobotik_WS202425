# Exports
export ROS_LOCALHOST_ONLY=1
export ROS_DOMAIN_ID=80
export WEBOTS_HOME=/usr/local/webots
export CRAZYFLIE_ID=1

# Alias
# alias sendTarget="ros2 topic pub /safeflie0/send_target crazyflies_interfaces/msg/SendTarget \"p" --> Use Autocomplete
alias takeoff="ros2 topic pub /safeflie${CRAZYFLIE_ID}/takeoff std_msgs/Empty --once"
alias land="ros2 topic pub /safeflie${CRAZYFLIE_ID}/land std_msgs/Empty --once"
alias launch-webots="ros2 launch roboss tha_framework.launch.py type:=2 backend:=webots id:=0"
alias launch-hardware="ros2 launch roboss tha_framework.launch.py type:=1 backend:=hardware"
alias run-node="ros2 run roboss roboss"
alias build="colcon build"
alias cfclient="python3 ~/crazyflie-clients-python/bin/cfclient"
# Specify controller python script at the end
alias webots-controller="$WEBOTS_HOME/webots-controller --protocol=tcp --ip-address=127.0.0.1 --port=1234 --robot-name=cf0_ros_ctrl"

source ~/ds-crazyflies/install/setup.bash
source /opt/ros/humble/setup.bash
source ./install/setup.bash