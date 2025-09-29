#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class ImageBinaryNode(Node):
    def __init__(self):
        super().__init__('image_binary_node')
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT, history=HistoryPolicy.KEEP_LAST)
        self.bridge = CvBridge()
        self.sub = self.create_subscription(Image, '/image_raw', self.cb, qos)
        self.pub = self.create_publisher(Image, '/image_binary', qos)
        self.get_logger().info('image_binary_node listo (sub: /image_raw → pub: /image_binary)')

    def cb(self, msg: Image):
        try:
            # intenta BGR, si falla prueba RGB
            cv = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception:
            cv = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
            cv = cv[..., ::-1]  # RGB->BGR

        gray = cv2.cvtColor(cv, cv2.COLOR_BGR2GRAY)
        _, bw = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

        out = self.bridge.cv2_to_imgmsg(bw, encoding='mono8')
        out.header = msg.header  # conserva timestamp/frame_id
        self.pub.publish(out)

def main():
    rclpy.init()
    node = ImageBinaryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
