# Classical Computer Vision: Lane Line Extractor

This project is a lane line detection pipeline built with Python, OpenCV, and NumPy. It processes static highway road images to identify and isolate lane boundaries using classical computer vision techniques.

---

## Processing Pipeline

The pipeline processes each road image through five sequential stages:

1. **Image Loading (`load_image`)**: Reads the input image into memory in BGR format.
2. **HSV Color Filtering (`filter_colors`)**: Converts BGR to HSV color space and applies threshold masks to isolate yellow and white painted lane markings while ignoring dark asphalt and shadows.
3. **Gaussian Smoothing (`apply_blur`)**: Softens the image using a 5x5 Gaussian kernel to remove high-frequency noise and asphalt texture.
4. **Canny Edge Detection (`detect_edges`)**: Detects sharp intensity changes to trace thin, 1-pixel-wide outlines of the lane lines using dual-threshold hysteresis.
5. **Region of Interest (ROI) Masking (`apply_roi`)**: Applies a dynamic trapezoidal mask to keep only the road corridor directly in front of the vehicle, removing edges from the sky, trees, and horizon.

---

## Requirements & Setup

- Python 3.10+
- OpenCV (`opencv-python`)
- NumPy

### Installation

```bash
pip install opencv-python numpy
```

---

## How to Run

1. Place your test images inside the `test_images/` directory.
2. Run the script from the project root:

```bash
python lane_extractor.py
```

The extracted output images will automatically be saved into the `outputs/` folder.