import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

def binary_mapping(image_path):
    # Read the image
    image = cv2.imread(image_path)
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    # Apply adaptive thresholding
    binary = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 1)
    # Apply morphological operations to fill gaps
    kernel = np.ones((8, 6), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    return binary

def find_landmarks(binary_image):
    # Find contours
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Assuming the largest contour is the hand
    hand_contour = max(contours, key=cv2.contourArea)
    # Find convex hull and convexity defects
    hull_indices = cv2.convexHull(hand_contour, returnPoints=False)
    defects = cv2.convexityDefects(hand_contour, hull_indices)
    
    # Convert hull indices to points
    hull_points = [tuple(hand_contour[idx][0]) for idx in hull_indices.flatten()]
    
    # Identify key points: fingertips and base of the hand
    landmarks = []
    if defects is not None:
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(hand_contour[s][0])
            end = tuple(hand_contour[e][0])
            far = tuple(hand_contour[f][0])
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
    
    # Filter out points that are too far from the convex hull (likely on the arm)
    unique_landmarks = [point for point in unique_landmarks if cv2.pointPolygonTest(np.array(hull_points), (int(point[0]), int(point[1])), True) > -50]

    return hand_contour, unique_landmarks

def draw_skeleton(image, hand_contour, landmarks):
    # Draw hand contour
    cv2.drawContours(image, [hand_contour], -1, (0, 255, 0), 2)
    # Draw landmarks
    for point in landmarks:
        cv2.circle(image, point, 5, (0, 0, 255), -1)
    # Connect landmarks with edges
    for i in range(len(landmarks)):
        for j in range(i + 1, len(landmarks)):
            cv2.line(image, landmarks[i], landmarks[j], (255, 0, 0), 1)
    return image

def main(image_path):
    binary = binary_mapping(image_path)
    hand_contour, landmarks = find_landmarks(binary)
    original_image = cv2.imread(image_path)
    skeleton_image = draw_skeleton(original_image, hand_contour, landmarks)
    
    # Display results
    plt.figure(figsize=(10, 10))
    plt.subplot(1, 3, 1)
    plt.title('Original Image')
    plt.imshow(cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB))
    
    plt.subplot(1, 3, 2)
    plt.title('Binary Image')
    plt.imshow(binary, cmap='gray')
    
    plt.subplot(1, 3, 3)
    plt.title('Skeleton Image')
    plt.imshow(cv2.cvtColor(skeleton_image, cv2.COLOR_BGR2RGB))
    
    plt.show()

# Path to the JPEG image of a hand
image_path = 'hand.jpg'
main(image_path)
