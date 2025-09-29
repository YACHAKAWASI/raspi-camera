cat > docker/camera.Dockerfile <<'DOCKER'
FROM ros:humble-ros-base-jammy
SHELL ["/bin/bash","-c"]

# ROS2 + cámara + cv_bridge + OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-humble-v4l2-camera ros-humble-image-tools ros-humble-cv-bridge \
    python3-opencv \
    && rm -rf /var/lib/apt/lists/*

ENV RMW_IMPLEMENTATION=rmw_fastrtps_cpp
WORKDIR /app

# Copiamos el nodo Python
COPY docker/image_binary.py /app/image_binary.py

# Ejecuta ambos: v4l2_camera y el nodo Python
CMD source /opt/ros/humble/setup.bash && \
    (ros2 run v4l2_camera v4l2_camera_node --ros-args -p camera_frame_id:=camera_v2 &) && \
    python3 /app/image_binary.py
DOCKER
