import cv2
import numpy as np
import matplotlib.pyplot as plt

# Color ranges in CrCb with higher saturation requirements
COLOR_RANGES = {
    'blue': {
        'lower': np.array([0, 80, 150]),  # Increased saturation minimum
        'upper': np.array([180, 150, 200])
    },
    'red': {
        'lower': np.array([10, 170, 80]),    # Increased saturation minimum
        'upper': np.array([180, 240, 120])
    },
    'yellow': {
        'lower': np.array([100, 120, 30]),   # Hue, Saturation, Value
        'upper': np.array([250, 200, 80])
    }
}

def detect_color_rectangles(image_path, target_color='blue'):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Could not read image {image_path}")
        return None
    
    # Convert to CrCb color space
    CrCb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    
    # Create mask based on color
    color_mask = cv2.inRange(CrCb, COLOR_RANGES[target_color]['lower'], COLOR_RANGES[target_color]['upper'])
    
    # Apply morphological operations to clean up the mask
    kernel = np.ones((5,5), np.uint8)
    color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, kernel)
    color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, kernel)
    
    # Find contours in the color mask
    contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create copies of the original image for visualization
    color_masked = cv2.bitwise_and(image, image, mask=color_mask)
    result_image = image.copy()
    quadrilaterals = []
    
    # Process each contour
    for contour in contours:
        # Filter small contours
        area = cv2.contourArea(contour)
        if area < 500:  # Increased minimum area for better filtering
            continue
        
        # Find the minimum area rectangle (can be rotated)
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int32(box)
        
        # Calculate aspect ratio of the rectangle
        width = np.linalg.norm(box[0] - box[1])
        height = np.linalg.norm(box[1] - box[2])
        aspect_ratio = max(width, height) / (min(width, height) + 1e-6)
        
        # Filter out extremely elongated shapes (adjust threshold as needed)
        if aspect_ratio > 5:
            continue
            
        quadrilaterals.append(box)
        # Draw the rotated rectangle
        cv2.drawContours(result_image, [box], 0, (0, 255, 0), 5)
        cv2.drawContours(color_masked, [box], 0, (0, 255, 0), 2)
    
    return result_image, color_masked, len(quadrilaterals)

def process_images(target_color='blue'):
    image_files = ['data1.png', 'data2.png', 'data3.png']
    
    # Create a figure with subplots for all images
    fig, axes = plt.subplots(len(image_files), 3, figsize=(20, 5*len(image_files)))
    
    for idx, image_path in enumerate(image_files):
        # Read original image
        original = cv2.imread(image_path)
        if original is None:
            print(f"Error: Could not read image {image_path}")
            continue
            
        # Convert BGR to RGB for matplotlib
        original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        
        # Detect rectangles
        result, color_masked, num_rectangles = detect_color_rectangles(image_path, target_color)
        if result is not None:
            result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
            masked_rgb = cv2.cvtColor(color_masked, cv2.COLOR_BGR2RGB)
            
            # Plot original, color mask, and result images
            axes[idx, 0].imshow(original_rgb)
            axes[idx, 0].set_title(f'Original: {image_path}')
            axes[idx, 0].axis('off')
            
            axes[idx, 1].imshow(masked_rgb)
            axes[idx, 1].set_title(f'Color Mask ({target_color})')
            axes[idx, 1].axis('off')
            
            axes[idx, 2].imshow(result_rgb)
            axes[idx, 2].set_title(f'Detected Rectangles: {num_rectangles} {target_color} rectangles')
            axes[idx, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig(f'color_rectangle_detection_{target_color}.png')
    plt.close()
    
    print(f"\nProcessing complete! Results saved as 'color_rectangle_detection_{target_color}.png'")

if __name__ == "__main__":
    # You can change the target color to 'red', 'blue', or 'yellow'
    process_images(target_color='yellow') 