import numpy as np
from PIL import Image

def load_image(path):
    with Image.open(path) as img:
        return np.array(img)

# Load your images
image_paths = ['2019/2019_comp_clip.tif', '2021/2021_comp_clip.tif', '2022/2022_comp_clip.tif', '2023/2023_comp_clip.tif']
images = [load_image(path) for path in image_paths]

# Determine the maximum extent
max_width = max(img.shape[1] for img in images)
max_height = max(img.shape[0] for img in images)

# Initialize an empty array and a count array
composite = np.zeros((max_height, max_width), dtype=np.float32)
count = np.zeros((max_height, max_width), dtype=np.float32)

# Aggregate and average
for img in images:
    h, w = img.shape
    composite[:h, :w] += img
    count[:h, :w] += 1

# Avoid division by zero
count[count == 0] = 1
composite /= count

# Convert back to an image and save
result = Image.fromarray(np.uint8(composite))
result.save('results/LST_composite_image.tif')