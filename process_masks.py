import numpy as np
from argparse import ArgumentParser
from PIL import Image
import os

def threshold(img, threshold=0.1):
    img = (img > threshold).astype(int)
    return img

if __name__ == "__main__":
    parser = ArgumentParser(description='Process masks')
    parser.add_argument('-d', '--directory', required=True, help='Mask directory')
    args = parser.parse_args()
    mask_dir = args.directory

    for mask in os.listdir(mask_dir):
        mask_path = os.path.join(mask_dir, mask)
        mask_image = np.asarray(Image.open(mask_path))
        
        # print("Unique values before threshold:", np.unique(mask_image))        
        mask_image = threshold(mask_image)        
        # print("Unique values after threshold:", np.unique(mask_image))
        
        mask_image = Image.fromarray(mask_image.astype(np.uint8))
        mask_image.save(mask_path)