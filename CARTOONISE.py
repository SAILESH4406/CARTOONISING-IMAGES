import streamlit as st
from PIL import Image
import numpy as np
import cv2

def cartoonize_image(image):
    # Convert image to numpy array
    img_array = np.array(image)

    # Convert image to grayscale
    gray = cv2.cvtColor(img_array, cv2.COLOR_BGR2GRAY)
    
    # Apply median blur to reduce noise
    gray_blurred = cv2.medianBlur(gray, 5)
    
    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(
        gray_blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    
    # Apply bilateral filter to reduce color palette
    color = cv2.bilateralFilter(img_array, d=9, sigmaColor=250, sigmaSpace=250)
    
    # Create a sketch effect by combining edges with the color image
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    
    # Further enhance the cartoon effect by applying a stylization filter
    cartoon = cv2.stylization(cartoon, sigma_s=150, sigma_r=0.25)
    
    
    return cartoon

st.title("Image to Cartoon Converter")
st.write("Upload an image to convert it into a cartoon.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    
    if st.button("Convert to Cartoon"):
        st.write("Converting...")
        cartoon_image = cartoonize_image(image)
        st.image(cartoon_image, caption='Cartoon Image', use_column_width=True)


