import cv2
import numpy as np
import os

# Step 1: Read the image file
def load_image(path):
    img = cv2.imread(path)
    if img is None:
        print("Image not found:", path)
    return img

# Step 2: Keep only yellow and white colors
def filter_colors(img):
    # Convert image from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Range for yellow
    lower_yellow = np.array([15, 80, 100])
    upper_yellow = np.array([30, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    
    # Range for white
    lower_white = np.array([0, 0, 190])
    upper_white = np.array([179, 40, 255])
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    
    # Combine both colors together
    combined_mask = cv2.bitwise_or(yellow_mask, white_mask)
    return combined_mask

# Step 3: Blur to remove noise
def apply_blur(img):
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    return blurred

# Step 4: Find the lines/edges
def detect_edges(img):
    edges = cv2.Canny(img, 50, 150)
    return edges

# Step 5: Cut out only the road area (trapezoid shape)
def apply_roi(img):
    h = img.shape[0]
    w = img.shape[1]
    
    # Make a blank black image
    mask = np.zeros_like(img)
    
    # Coordinates of the road area
    points = np.array([
        [
            (int(w * 0.05), h),               # bottom left
            (int(w * 0.45), int(h * 0.60)),   # top left
            (int(w * 0.55), int(h * 0.60)),   # top right
            (int(w * 0.95), h)                # bottom right
        ]
    ], dtype=np.int32)
    
    # Draw white polygon on the mask
    cv2.fillPoly(mask, points, 255)
    
    # Keep only what is inside the polygon
    result = cv2.bitwise_and(img, mask)
    return result

# Run everything here

if __name__ == "__main__":
    # Create the output folder if it doesn't exist
    if not os.path.exists("outputs"):
        os.makedirs("outputs")

    input_folder = "test_images"
    
    # Get all file names inside test_images folder
    all_files = os.listdir(input_folder)

    # Filter to only pick image files
    image_files = [f for f in all_files if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    print(f"Found {len(image_files)} images to process.\n")

    for filename in image_files:
        image_path = os.path.join(input_folder, filename)
        name_without_ext = os.path.splitext(filename)[0]

        print(f"--> Processing: {filename}")

        # Run the 5-step pipeline
        img = load_image(image_path)
        colors = filter_colors(img)
        blurred = apply_blur(colors)
        edges = detect_edges(blurred)
        final_lanes = apply_roi(edges)

        # Save all steps to outputs folder with the image's name
        cv2.imwrite(f"outputs/{name_without_ext}_1_original.jpg", img)
        cv2.imwrite(f"outputs/{name_without_ext}_2_colors.jpg", colors)
        cv2.imwrite(f"outputs/{name_without_ext}_3_blurred.jpg", blurred)
        cv2.imwrite(f"outputs/{name_without_ext}_4_edges.jpg", edges)
        cv2.imwrite(f"outputs/{name_without_ext}_5_final_lanes.jpg", final_lanes)

        # Show the final result on screen
        cv2.imshow(f"Final Lanes - {filename}", final_lanes)
        print("    Press any key (or Enter) on the image window to continue to the next image...")
        
        # Wait for user input to move to the next image
        cv2.waitKey(0)
        
        # Close the current window before opening the next
        cv2.destroyAllWindows()

    print("\nAll images processed successfully! Check the outputs folder.")