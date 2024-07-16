import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

def load_image(rgb_path):
    # Load the RGB image
    rgb_image = cv2.imread(rgb_path)
    return rgb_image

def create_silhouette(rgb_image):
    # Convert RGB image to grayscale
    gray = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Thresholding to create a binary silhouette
    _, binary_silhouette = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Morphological operations to clean up the silhouette
    kernel = np.ones((5, 5), np.uint8)
    silhouette = cv2.morphologyEx(binary_silhouette, cv2.MORPH_CLOSE, kernel)
    
    return silhouette

def extract_rgb_landmarks(rgb_image):
    # Convert to grayscale
    gray = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    
    # Adaptive thresholding to create a binary image
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    # Morphological operations to clean up the binary image
    kernel = np.ones((5, 5), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    #binary = cv2.resize(binary, (binary.shape[1] // 2, binary.shape[0] // 2))

    height, width = binary.shape
    roi = binary[:height * 3 // 5, :]
    
    # Find contours and convex hull
    contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hand_contour = max(contours, key=cv2.contourArea)
    hull_indices = cv2.convexHull(hand_contour, returnPoints=False)
    defects = cv2.convexityDefects(hand_contour, hull_indices)

    # Identify key points: fingertips and base of the hand
    landmarks = []
    if defects is not None:
        for i in range(len(defects)):
            s, e, f, d = defects[i, 0]
            start = tuple(hand_contour[s][0])
            end = tuple(hand_contour[e][0])
            landmarks.extend([start, end])
    
    # Remove duplicate points
    landmarks = list(set(landmarks))
    
    # Convert landmarks to a numpy array for clustering
    landmarks_array = np.array(landmarks)
    
    # Apply DBSCAN clustering to combine nearby points
    clustering = DBSCAN(eps=21, min_samples=1).fit(landmarks_array)
    unique_landmarks = []
    for cluster_id in set(clustering.labels_):
        cluster_points = landmarks_array[clustering.labels_ == cluster_id]
        # Compute the average point of the cluster
        mean_point = np.mean(cluster_points, axis=0)
        unique_landmarks.append(tuple(mean_point.astype(int)))
    
    # Ensure we have exactly 5 fingertips
    if len(unique_landmarks) > 5:
        unique_landmarks = sorted(unique_landmarks, key=lambda x: x[1])[:5]
    
    # Find the base of the palm by taking the bottom-most point in the hand contour
    base_palm = tuple(max(hand_contour, key=lambda x: x[0][1])[0])
    unique_landmarks.append(base_palm)
    
    return hand_contour, unique_landmarks

def draw_skeleton(rgb_image, hand_contour, landmarks):
    # Draw hand contour
    cv2.drawContours(rgb_image, [hand_contour], -1, (0, 255, 0), 2)
    # Draw landmarks
    for point in landmarks:
        cv2.circle(rgb_image, point, 5, (0, 0, 255), -1)
    
    # Connect fingertips to the base of the palm
    base_palm = max(landmarks, key=lambda x: x[1])
    for point in landmarks:
        if point != base_palm:
            cv2.line(rgb_image, point, base_palm, (255, 0, 0), 2)

    return rgb_image

def main(rgb_path):
    # Load RGB image
    rgb_image = load_image(rgb_path)
    
    # Process RGB image to extract landmarks
    hand_contour, landmarks = extract_rgb_landmarks(rgb_image)
    
    # Create silhouette from RGB image
    silhouette = create_silhouette(rgb_image)
    
    # Draw skeleton over the original RGB image
    skeleton_image = draw_skeleton(rgb_image.copy(), hand_contour, landmarks)
    
    # Display results
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 3, 1)
    plt.title('Original RGB Image')
    plt.imshow(cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB))
    
    plt.subplot(1, 3, 2)
    plt.title('Silhouette Image')
    plt.imshow(silhouette, cmap='gray')
    
    plt.subplot(1, 3, 3)
    plt.title('Skeleton Image')
    plt.imshow(cv2.cvtColor(skeleton_image, cv2.COLOR_BGR2RGB))
    
    plt.tight_layout()
    plt.show()

# Path to the RGB image
rgb_path = 'hand.jpg'
main(rgb_path)
