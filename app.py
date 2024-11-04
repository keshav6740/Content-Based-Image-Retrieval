from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
import os
from sklearn.neighbors import NearestNeighbors
from cbir import load_images_from_folder, extract_features, build_index, retrieve_similar_images  # Import functions

app = Flask(__name__)
CORS(app)

# Load and pre-process images once
images = load_images_from_folder('jpg')
feature_list = extract_features(images, method='ORB')
index, filtered_feature_list = build_index(feature_list)

@app.route('/search', methods=['POST'])
def search_similar_images():
    file = request.files.get('image')
    if not file:
        return jsonify({"error": "No image provided"}), 400

    # Read the image and find similar images
    file_bytes = np.frombuffer(file.read(), np.uint8)
    query_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    similar_images = retrieve_similar_images(query_image, filtered_feature_list, index, method='ORB')
    if similar_images:
        similar_images = [{"path": img_path} for img_path in similar_images]
    else:
        similar_images = []

    return jsonify(similar_images)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
