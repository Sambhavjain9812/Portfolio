import cv2
import numpy as np
import urllib.request
import matplotlib.pyplot as plt

# Image URL
url = "https://upload.wikimedia.org/wikipedia/commons/6/6a/JavaScript-logo.png"

# Download the image as an array of bytes
resp = urllib.request.urlopen(url)
image_array = np.asarray(bytearray(resp.read()), dtype=np.uint8)

# Decode image into OpenCV format
image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

# Convert BGR to RGB (for correct colors in matplotlib)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
image= cv2.resize(src=image, dsize=2)
# Display the image
plt.imshow(image)
plt.axis("off")
plt.show()
