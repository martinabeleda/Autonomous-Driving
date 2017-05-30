import cv2
import numpy as np
import matplotlib.pyplot as plt

from region_of_interest import region_of_interest
from draw_lines import draw_lines

def lane_detect(img):
    """
    Detects lanes in an image.

    Applies gaussian blur, canny edge detection,
    removes false negatives, hough lines and then
    combines small lines into 2 lanes. Draws the lanes
    on the original image.

    Outputs:
        img - The original image with the lane centre line (green), lanes (cyan),
            frame centre line (blue) and angle, d_top and d_bot overlayed.
        angle - The angle of the centre line from the vertical. The angle
            indicates the horizontal position of the robot in the lanes. Positive
            angle corresponds to displacement to the right of the lane and vice
            versa.
        topDisplacement - Top displacement indicates the angle that the robot
            is heading. Positive topDisplacement corresponds to the robot pointing
            to the right and vice versa.
        bottomDisplacement - Bottom displacement seems to be affected by both the
            angle and horizontal position of the robot so is not a good indicator
            of either.
    """

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Canny Edge Detection
    lowThreshold = 150
    highThreshold = 200
    edges = cv2.Canny(blur, lowThreshold, highThreshold)

    # Mask out areas outside region of interest
    # Region of interest is defined as a trapezoid to account for perspective
    lowerLeftPoint = [0, 600]
    middleLeftPoint = [0, 450]
    upperLeftPoint = [250, 300]
    upperRightPoint = [550, 300]
    middleRightPoint = [800, 450]
    lowerRightPoint = [800, 600]
    pts = np.array([[lowerLeftPoint, middleLeftPoint, upperLeftPoint,
                   upperRightPoint, middleRightPoint, lowerRightPoint]], dtype=np.int32)
    roi = region_of_interest(edges, pts)

    # Remove false negatives
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(roi, cv2.MORPH_CLOSE, kernel)

    # Hough Lines
    rho = 1
    theta = np.pi/180
    threshold = 30
    minLineLength = 20
    maxLineGap = 20
    lines = cv2.HoughLinesP(closing, rho, theta, threshold,
                          minLineLength, maxLineGap)

    masked = region_of_interest(img, pts)

    try:
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv2.line(masked, (x1, y1), (x2, y2), [0, 0, 255], thickness=2)
    except:
        pass

    # Display hough lines
    (angle, topDisplacement, bottomDisplacement) = draw_lines(img, lines)

    # Display center line
    cv2.line(img, (400, 0), (400, 600), (255, 0, 0), thickness=2)

    return img, angle, topDisplacement, bottomDisplacement
