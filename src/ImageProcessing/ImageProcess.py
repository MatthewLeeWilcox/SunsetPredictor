import pandas as pd
import numpy as np
import cv2


image = cv2.imread('TestImage.jpg')

height, width, channels = image.shape

# Print the dimensions
print("Width:", width)
print("Height:", height)
print("Number of channels:", channels)


center = (width // 2, height // 2)

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
cv2.imshow('Result', result)
cv2.waitKey(0)
cv2.destroyAllWindows()