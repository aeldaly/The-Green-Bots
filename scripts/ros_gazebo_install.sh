sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
sudo apt-get update
sudo apt-get install ros-kinetic-desktop-full
sudo apt-get install ros-kinetic-joy ros-kinetic-teleop-twist-joy ros-kinetic-teleop-twist-keyboard ros-kinetic-laser-proc ros-kinetic-rgbd-launch ros-kinetic-rosserial-arduino ros-kinetic-rosserial-python ros-kinetic-rosserial-server ros-kinetic-rosserial-client kinetic-rosserial-msgs ros-kinetic-amcl ros-kinetic-map-server ros-kinetic-move-base ros-kinetic-urdf ros-kinetic-xacro kinetic-compressed-image-transport ros-kinetic-rqt-image-view ros-kinetic-gmapping ros-kinetic-navigation ros-kinetic-interactive-markers
mkdir -p /opt/bots/catkin_ws/src
git clone https://github.com/ROBOTIS-GIT/turtlebot3.git /opt/bots/catkin_ws/src
git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git /opt/bots/catkin_ws/src
git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git /opt/bots/catkin_ws/src
cd /opt/bots/catkin_ws/;
echo "/opt/ros/kinetic/setup.bash" >> ~/.bashrc
source ~/.bashrc
catkin_make
source devel/setup.bash
export TURTLEBOT3_MODEL=waffle_pi
# roslaunch turtlebot3_gazebo turtlebot3_simulation.launch
sudo rosdep init
rosdep update
roslaunch turtlebot3_gazebo turtlebot3_world.launch
