import pandas as pd
import numpy as np
import cv2
import os
from tqdm import tqdm
0
def list_files_in_folder(folder_path):
    files = os.listdir(folder_path)
    return files

def correctImg(filepath):

    image = cv2.imread(filepath)

    height, width, channels = image.shape

    center = (width // 2, height // 2)

    top = (height - width) // 2
    bottom = height - top


    # Define a point on the edge of the image (e.g., the rightmost edge)
    edge_point = (width - 1, height // 2)

    # Calculate the distance between the center and the edge point
    radius = int(np.sqrt((edge_point[0] - center[0])**2 + (edge_point[1] - center[1])**2))

    # Create a black mask
    mask = np.zeros((height, width), dtype=np.uint8)

    # Draw the circle on the mask
    cv2.circle(mask, center, radius, (255), -1)

    # Apply the mask to the image
    result = cv2.bitwise_and(image, image, mask=mask)

    # Display the result
    # cv2.imshow('Result', result)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    cv2.imwrite(filepath,result[top:bottom, :])

filepathway = list_files_in_folder('SunSetImg')

for file in tqdm(filepathway):
    filePath = "SunSetImg/" + file
    correctImg(filePath)


