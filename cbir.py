import cv2
import numpy as np
from sklearn.neighbors import NearestNeighbors
import glob
import os

# Load images from folder
def load_images_from_folder(folder_path):
    images = []
    for filename in glob.glob(os.path.join(folder_path, "*.jpg")):  # Adjust extension if needed
        img = cv2.imread(filename)
        if img is not None:
            images.append((filename, img))
    return images

# Extract features from images
def extract_features(images, method='ORB'):
    feature_list = []
    for filename, img in images:
        if method == 'ORB':
            descriptor = cv2.ORB_create()
        elif method == 'SIFT':
            descriptor = cv2.SIFT_create()
        else:
            raise ValueError("Descriptor method not recognized.")
            
        keypoints, features = descriptor.detectAndCompute(img, None)
        feature_list.append((filename, features))
    return feature_list

# Build the feature index for NearestNeighbors
def build_index(features):
    filtered_features = [(filename, f) for filename, f in features if f is not None and len(f) > 0]
    if not filtered_features:
        raise ValueError("No valid features found to build the index.")
    
    # Stack feature vectors into a 2D array
    feature_vectors = np.vstack([f for _, f in filtered_features])
    index = NearestNeighbors(n_neighbors=5, algorithm='brute', metric='euclidean')
    index.fit(feature_vectors)
    return index, filtered_features

# Retrieve similar images based on query image
def retrieve_similar_images(query_image, feature_list, index, method='ORB'):
    if method == 'ORB':
        descriptor = cv2.ORB_create()
    elif method == 'SIFT':
        descriptor = cv2.SIFT_create()
    
    # Extract features for the query image
    query_keypoints, query_features = descriptor.detectAndCompute(query_image, None)
    if query_features is None:
        print("No features found in the query image.")
        return []

    # Retrieve similar images using NearestNeighbors
    distances, indices = index.kneighbors(query_features)
    similar_images = [feature_list[i][0] for i in indices.flatten() if i < len(feature_list)]
    
    # Remove duplicates and limit to top results
    similar_images = list(dict.fromkeys(similar_images))[:5]  # Limit to top 5 unique images
    return similar_images

# Main execution code
if __name__ == "__main__":
    # Load images
    images = load_images_from_folder('jpg')
    print(f"Total images loaded: {len(images)}")

    # Extract features from images
    feature_list = extract_features(images, method='ORB')

    # Build index and get filtered feature list
    index, filtered_feature_list = build_index(feature_list)

    # Load a query image
    query_image_path = 'test.jpg'
    query_image = cv2.imread(query_image_path)

    if query_image is not None:
        # Retrieve similar images
        similar_images = retrieve_similar_images(query_image, filtered_feature_list, index, method='ORB')

        # Output the results
        print(f"Total valid feature vectors: {len([f for _, f in filtered_feature_list if f is not None])}")
        print("Similar images:")
        for img_path in similar_images:
            print(img_path)
            img = cv2.imread(img_path)
            if img is not None:
                cv2.imshow("Similar Image", img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
    else:
        print("Query image could not be loaded. Check the path or file format.")
