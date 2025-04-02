import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from clover import srv
from std_srvs.srv import Trigger
import math

get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
navigate_global = rospy.ServiceProxy('navigate_global', srv.NavigateGlobal)
set_position = rospy.ServiceProxy('set_position', srv.SetPosition)
set_velocity = rospy.ServiceProxy('set_velocity', srv.SetVelocity)
set_attitude = rospy.ServiceProxy('set_attitude', srv.SetAttitude)
set_rates = rospy.ServiceProxy('set_rates', srv.SetRates)
land = rospy.ServiceProxy('land', Trigger)

bridge = CvBridge()
rospy.init_node("TEST")
pub = rospy.Publisher('STATION', Image)


def navigate_wait(x=0, y=0, z=1.5, yaw=math.nan, speed=0.5, frame_id='aruco_map', tolerance=0.2, auto_arm=False):
    res = navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    if not res.success:
        return res

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            return res
        rospy.sleep(0.2)


def color_detect(data):
    img = bridge.imgmsg_to_cv2(data, 'bgr8')
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Detect green areas (healthy)
    green_lower = np.array([35, 100, 100])
    green_upper = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, green_lower, green_upper)

    # Detect red areas (virus)
    red_lower = np.array([0, 100, 100])
    red_upper = np.array([10, 255, 255])
    red_mask = cv2.inRange(hsv, red_lower, red_upper)

    # Combine both masks
    combined_mask = cv2.bitwise_or(green_mask, red_mask)

    # Find contours for green (healthy) areas
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in green_contours:
        if cv2.contourArea(contour) > 500:
            cv2.drawContours(img, [contour], -1, (255, 0, 0), 2)
            x, y, w, h = cv2.boundingRect(contour)
            cv2.putText(img, "healthy", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2,
                        cv2.LINE_AA)

    # Find contours for red (virus) areas
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in red_contours:
        if cv2.contourArea(contour) > 500:
            cv2.drawContours(img, [contour], -1, (0, 255, 255), 2)
            x, y, w, h = cv2.boundingRect(contour)
            cv2.putText(img, "virus", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2,
                        cv2.LINE_AA)

    pub.publish(bridge.cv2_to_imgmsg(img, 'bgr8'))


if __name__ == '__main__':
    print('Started')
    image_sub = rospy.Subscriber('main_camera/image_raw_throttled', Image, color_detect, queue_size=1)
    rospy.sleep(4)
    navigate_wait(frame_id='body', auto_arm=True)
    rospy.sleep(2)
    navigate_wait(x=1, y=2, frame_id='aruco_map')
    navigate_wait(x=3, y=1, frame_id='aruco_map')
    navigate_wait(x=0, y=0, frame_id='aruco_map')
    land()
