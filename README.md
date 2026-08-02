# Document Scanner (OpenCV + Python)

A small computer-vision tool that turns a photo of a piece of paper (receipt, page, etc.) into a clean, top-down "scanned" image. It works in three steps: detect edges, find the four-cornered contour of the document, then apply a perspective transform and adaptive thresholding to get a flat, black-and-white scan.

## How it works

**`transform.py`**
- `order_points(pts)` — Takes four arbitrary `(x, y)` points and sorts them into a consistent order: top-left, top-right, bottom-right, bottom-left. Top-left/bottom-right come from the sum of each point's coordinates (smallest sum = top-left, largest = bottom-right); top-right/bottom-left come from the difference of each point's coordinates (smallest diff = top-right, largest = bottom-left).
- `four_point_transformation(image, pts)` — Orders the four points, computes the output width/height from the maximum distances between corners, builds the destination rectangle, and uses `cv2.getPerspectiveTransform` + `cv2.warpPerspective` to produce a straightened, top-down crop of the region.

**`scan.py`** — the driver script:
1. **Edge detection** — loads the image, resizes it to a height of 500px (for speed/accuracy, tracking the resize `ratio` so the transform can later be applied to the full-resolution original), converts to grayscale, blurs it, and runs Canny edge detection.
2. **Contour detection** — finds contours in the edge map, keeps the 5 largest by area, and picks the first one that approximates to exactly 4 points (`cv2.approxPolyDP`) — the assumption being that the largest 4-point contour is the sheet of paper.
3. **Perspective transform + threshold** — feeds the detected 4-point contour (scaled back up by `ratio`) into `four_point_transformation` on the *original* full-resolution image, then converts the warped result to grayscale and applies scikit-image's `threshold_local` (Gaussian adaptive thresholding) to give it a clean black-and-white "scanned document" look.

At each step the script displays the intermediate images (`cv2.imshow`) so you can see edge detection, the detected outline, and the final scan.

## Project structure

```
transform.py    # order_points() and four_point_transformation()
scan.py         # CLI driver: edge detection -> contour -> perspective transform -> threshold
images/         # input images to scan
```

## Requirements

- Python 2.7 / 3+
- OpenCV 2.4 / 3+
- NumPy
- [imutils](https://pypi.org/project/imutils/) (for `imutils.resize` / `imutils.grab_contours`)
- [scikit-image](https://scikit-image.org/) (for `threshold_local`)

```bash
pip install --upgrade imutils scikit-image numpy opencv-python
```

## Usage

```bash
python scan.py --image images/receipt.jpg
```

The script pops up windows for each step — press any key to advance through them:

1. **Step 1** — original (resized) image and its Canny edge map.
2. **Step 2** — the image with the detected 4-point document outline drawn on it in green.
3. **Step 3** — the original image alongside the final warped, thresholded, black-and-white scan.

## Notes & limitations

- The scanner assumes the document is the *largest* 4-point contour in the image — it won't work well if the background is cluttered with other large rectangular objects, or if the document's edges don't contrast enough with the background for Canny to pick them up cleanly.
- `cv2.findContours`'s return signature differs across OpenCV versions (2.4 vs. 3 vs. 4); if you hit an unpacking error, adjust how the result is unpacked for your installed OpenCV version.
- The `order_points` sum/difference heuristic works for typical rectangular documents but can misorder corners for unusual quadrilaterals or steep rotations.
- Output width/height are derived purely from pixel distances between the detected corners, so the aspect ratio isn't guaranteed to match the physical document — results can look stretched at steep viewing angles.
- No OCR is performed — this only produces a cleaned-up, flattened scan image.

## Credit

Based on the `four_point_transform` / document-scanner tutorials by Adrian Rosebrock, PyImageSearch:
- "4 Point OpenCV getPerspective Transform Example" (Aug 25, 2014)
- "How to Build a Kick-Ass Mobile Document Scanner in Just 5 Minutes" (Sep 1, 2014)
