import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    CrCb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    
    # Step 1: Thresholding - Black out all pixels that are not yellow
    lower_yellow = np.array([100, 120, 30])  # Lower bound for yellow in HSV
    upper_yellow = np.array([250, 200, 80])  # Upper bound for yellow in HSV
    threshold = cv2.inRange(CrCb, lower_yellow, upper_yellow)
    
    # Step 2: Masking - Fill in the remaining pixels from thresholding
    masked_image = cv2.bitwise_and(image, image, mask=threshold)

    # Apply morphological operations to clean up the mask
    kernel = np.ones((5,5), np.uint8)
    masked_image = cv2.morphologyEx(masked_image, cv2.MORPH_OPEN, kernel)
    
    # Step 3: Detecting Canny Edge - Create a wireframe of target objects
    edges = cv2.Canny(threshold, 50, 150)
    
    # Step 4: Dilating Edge - Emphasize the edges for better contour detection
    kernel = np.ones((3,3), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=2)
    
    # Step 5: Finding Contours - Identify closed shapes
    contours, _ = cv2.findContours(dilated_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw contours on the original image
    contour_image = image.copy()
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
    
    # Print contours to the console
    print(f"Detected {len(contours)} contours.")

    return contour_image, threshold, masked_image, edges, dilated_edges

def print_output():
    image_files = ['data1.png', 'data2.png']
    
    # Create a figure with subplots for all iamges 
    fig, axis = plt.subplots(len(image_files), 4, figsize=(20, 5*len(image_files)))

    for idx, image_path in enumerate(image_files):
        original = cv2.imread(image_path)
        if original is None:
            print(f"Error: Could not read image {image_path}")
            continue

        # Convert BGR to RGB for matplotlib
        original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)

        # Detect rectangles
        result, threshold, masked, edge, dilated_edges = process_image(image_path)
        if(result is not None):
            result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            threshold_rgb = cv2.cvtColor(threshold, cv2.COLOR_BGR2RGB)
            masked_rgb = cv2.cvtColor(masked, cv2.COLOR_BGR2RGB)
            edge_rgb = cv2.cvtColor(edge, cv2.COLOR_BGR2RGB)
            dilated_edges_rgb = cv2.cvtColor(dilated_edges, cv2.COLOR_BGR2RGB)
        
            # Display the results
            axis[idx, 0].imshow(original_rgb)
            axis[idx, 0].set_title("Original")
            axis[idx, 0].axis('off')
        
            axis[idx, 1].imshow(masked_rgb)
            axis[idx, 1].set_title("Masked image")
            axis[idx, 1].axis('off')

            axis[idx, 2].imshow(dilated_edges_rgb)
            axis[idx, 2].set_title("Dilated Edges")
            axis[idx, 2].axis('off')
        
            axis[idx, 3].imshow(result_rgb)
            axis[idx, 3].set_title("Final Image")
            axis[idx, 3].axis('off')

    plt.tight_layout()
    plt.savefig(f'color_rectangle_detection.png')
    plt.close()

if __name__ == "__main__":
    print_output()
