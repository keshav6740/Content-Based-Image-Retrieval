# Content-Based Image Retrieval (CBIR) System

This project is a Content-Based Image Retrieval (CBIR) system designed to retrieve images based on visual content, including features like color, texture, and shape. The system uses OpenCV for feature extraction and matches images by comparing these features to a pre-indexed database.

## Project Overview

The goal of this project is to create an efficient CBIR system that can retrieve relevant images based on a query image. By using feature extraction techniques, the system identifies similar images across various scenarios like object recognition, material identification, and texture-based retrieval.

### Key Features

- Extracts image features using color histograms, edge detection, and texture descriptors.
- Compares images based on visual content, bypassing the need for keyword or tag-based search.
- Optimized for high accuracy and fast retrieval across different scenarios.

## Dataset Setup

This project uses a subset of the **Oxford Flowers 102** dataset. Follow these steps to download and prepare the dataset:

1. **Download the Dataset:**
   - Visit the [Oxford Flowers 102 Dataset Page](https://www.robots.ox.ac.uk/~vgg/data/flowers/102/).
   - Scroll down to the **102 Category Flower Dataset** section.
   - Click on **"Dataset images (2 GB)"** to download the `.tgz` file.

2. **Extract the Dataset:**
   - After downloading, extract the `.tgz` file.
   - On Linux or macOS, use this command to extract:
     ```bash
     tar -xf 102flowers.tgz
     ```
   - On Windows, you can use extraction tools like **WinRAR** or **7-Zip**.

3. **Create a Subset of 100 Images:**
   - After extraction, navigate to the `jpg` folder, which contains all images.
   - Select 100 images manually or use the following Python code snippet to create a subset of 100 images:
