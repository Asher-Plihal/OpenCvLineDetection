import cv2
import numpy as np

# Color ranges in YCrCb with higher saturation requirements
COLOR_RANGES = {
    '1': { # red = 1
        'lower': np.array([10, 170, 80]),
        'upper': np.array([180, 240, 120])
    },
    '2': { # blue = 2
        'lower': np.array([0, 80, 150]),
        'upper': np.array([180, 150, 200])
    },
    '3': { # yellow = 3
        'lower': np.array([100, 120, 30]),
        'upper': np.array([250, 200, 80])
    }
}

def drawDecorations(image, text):
    cv2.putText(image, 
        text, 
        (0, 230), 
        cv2.FONT_HERSHEY_SIMPLEX, 
        1, (0, 255, 0), 1, cv2.LINE_AA)
    
# runPipeline() is called every frame by Limelight's backend.
def runPipeline(image, llrobot):

    contour_angle = None
    target_color = None
    corners = None

    try:
        # Check if we received data form the robot
        if len(llrobot) >= 5:
            target_color = int(llrobot[0]) # First value is target color
            corners = [(llrobot[1], llrobot[2]), (llrobot[3], llrobot[4])] # Last for is corners of the draw rect

        print(f"Target Color: {target_color}, Corners: {corners}")
        if target_color is not None and corners is not None:
            # Create mask for everything but detected objects rect
            mask = np.zeros_like(image)
            cv2.rectangle(mask, corners[0], corners[1], (255, 255, 255), -1) 
            masked_image = cv2.bitwise_and(image, mask)

            print(f"Color ranges: {COLOR_RANGES[str(target_color)]['lower']}, {COLOR_RANGES[str(target_color)]['upper']}")
            # Create mask based on target color
            YCrCb = cv2.cvtColor(masked_image, cv2.COLOR_BGR2YCrCb)
            color_mask = cv2.inRange(YCrCb, COLOR_RANGES[str(target_color)]['lower'], COLOR_RANGES[str(target_color)]['upper'])
   
            # Find contours from that target mask
            contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            print(f"Contours: {len(contours)}")
            if len(contours) > 0: 
                largestContour = float('-inf')
                for contour in contours:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int32(box)
                    cv2.drawContours(masked_image, [box], 0, (0, 255, 0), 2)

                    _ , (w , h), contour_angle = cv2.minAreaRect(contour)
                    area = w * h
                    if  area > largestContour:
                        largestContour = area
                        if(w < h):
                            contour_angle = contour_angle + 90
                        else:
                            contour_angle = contour_angle

            cv2.imshow('Masked Image first', masked_image)
            cv2.imshow('threshold Image', color_mask)
            cv2.imshow('Original Image', image)
            cv2.waitKey(0)

    except Exception as e:
        # If an error occurs, draw it on the image
        drawDecorations(image, f"Error: {str(e)}")
       
    # returning contour angle
    return contour_angle


if __name__ == "__main__":
    angle = runPipeline(cv2.imread('data1.png'), [3, 460, 750, 670, 975]) # Color, x1, y1, x2, y2
    print(f"Contour Angle: {angle}")