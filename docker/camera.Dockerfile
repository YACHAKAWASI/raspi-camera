FROM ros:humble-ros-base-jammy
SHELL ["/bin/bash","-c"]

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-v4l2-camera ros-humble-image-tools \
    && rm -rf /var/lib/apt/lists/*

ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp
WORKDIR /app

CMD source /opt/ros/humble/setup.bash && \
    ros2 run v4l2_camera v4l2_camera_node
