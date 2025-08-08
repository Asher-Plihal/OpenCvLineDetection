import cv2
import numpy as np
    
def runPipeline(image):

    corners = [(420, 550), (590, 675)]
    pt1 = (460, 750) # Top left corner
    pt2 = (670, 975) # Bottom right corner

    # Create mask for everything but detected objects rect
    mask = np.zeros_like(image)
    cv2.rectangle(mask, corners[0], corners[1], (255, 255, 255), -1) 
    masked_image = cv2.bitwise_and(image, mask)

    # Create mask based on target color
    YCrCb = cv2.cvtColor(masked_image, cv2.COLOR_BGR2YCrCb)
    color_mask = cv2.inRange(YCrCb, np.array([100, 120, 30]), np.array([250, 200, 80]))
   
    # Find contours from that target mask
    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(f"Contours: {len(contours)}")
    if len(contours) > 0: 
        largestContour = float('-inf')
        for contour in contours:
             # Used to draw the contours (can be removed when not needed)
             rect = cv2.minAreaRect(contour)
             box = cv2.boxPoints(rect)
             box = np.int32(box)
             cv2.drawContours(masked_image, [box], 0, (0, 255, 0), 2)
             
             _ , (width, height), contour_angle = cv2.minAreaRect(contour)
             area = cv2.contourArea(contour)
             print(f"Area: {area}")
             if  area > largestContour:
                largestContour = area
                print(f"widht: {width} < height: {height}")
                if(width < height):
                    print(f"Contour angle: {contour_angle}")
                    contour_angle = contour_angle + 90
                else:
                    print(f"New Contour angle: {contour_angle}")
                    contour_angle = contour_angle
       
    cv2.imshow('Masked Image first', masked_image)
    #cv2.imshow('threshold Image', color_mask)
    #cv2.imshow('Original Image', image)
    cv2.waitKey(0)

    # returning contour angle,
    # an image to stream
    return contour_angle, masked_image, color_mask


if __name__ == "__main__":
    angle, image, img_threshold = runPipeline(cv2.imread('data1.png')) # Color, x1, y1, x2, y2

    print(f"Contour Angle fianl: {angle}")