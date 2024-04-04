import numpy as np
import cv2 as cv
from argparse import ArgumentParser
from PIL import Image
import pandas as pd
import os
import urllib.parse

def threshold(img, intensity, threshold=0.1):
    img = (img > threshold).astype(np.uint8)
    return img * intensity

if __name__ == "__main__":
    parser = ArgumentParser(description='Process masks')
    parser.add_argument('-d', '--directory', required=True, help='Mask directory')
    parser.add_argument('-o', '--output', required=False, help='Output directory')
    parser.add_argument('-s', '--suffix', required=False, help='Suffix to add to the mask name', default='_mask')    
    parser.add_argument('-b', '--bindings', required=False, help='Csv file with bindings between masks and images (exported from LabelStudio)')
    parser.add_argument('-r', '--remove', required=False, help='Remove the original masks', default=False, action='store_true')
    args = parser.parse_args()
    mask_dir = args.directory

    save_dir = ""
    if args.output:
        save_dir = args.output
    else:
        save_dir = mask_dir

    print(save_dir)

    bindings_dict = {}
    if args.bindings:
        bindings = pd.read_csv(args.bindings, usecols=['annotation_id', 'image'])
        # Create a dictionary with the bindings, where the key is the task id and the value is the image path
        # Example: {'task_1': 'path/to/image_1.jpg', 'task_2': 'path/to/image_2.jpg'}
        # The dictionary is used to map the task id to the image name
        # The csv file is exported from LabelStudio
        bindings_dict = {k: v[0] for k, v in bindings.set_index('annotation_id').T.to_dict('list').items()}

        # Remove the path from the image name
        for k, v in bindings_dict.items():
            decoded_path = urllib.parse.unquote(v)
            bindings_dict[k] = os.path.basename(decoded_path)

    annotation_dict = {}
    
    for mask in os.listdir(mask_dir):
        mask_path = os.path.join(mask_dir, mask)
        
        # Extract the annotation value from the file name
        annotation = int(mask.split('-')[3])
        # Add the file path to the corresponding list in the dictionary
        if annotation not in annotation_dict:
            annotation_dict[annotation] = []
        
        annotation_dict[annotation].append(mask_path)

    class_intensity = {
        'Hot Spot': 1,
        'Third': 0,
        'Greenery': 1,
        'Row': 0,
    }

    # Combine the images
    for id in annotation_dict.keys():
        masks = annotation_dict[id]

        with Image.open(masks[0]) as img:
            size = np.asarray(img).shape
            combined_mask = np.zeros(size, dtype=np.uint8)
            print('Creating new mask')

        for mask in masks:
            mask_img = np.asarray(Image.open(mask))
            type = mask.split('-')[-2]

            mask_img = threshold(mask_img, class_intensity[type], 0.1)

            # Only consider pixels in the current mask that are not 0
            mask_img_non_zero = np.where(mask_img != 0, mask_img, combined_mask)

            # Use np.where to overwrite the pixel values where the new image is not zero
            combined_mask = np.where(combined_mask < class_intensity[type], mask_img_non_zero, combined_mask)
            print(f'Added {mask} \nType: {type}\nIntensity: {class_intensity[type]}')

            if args.remove:
                os.remove(mask)
                print(f'Removed {mask}')

        combined_mask = combined_mask.astype(np.uint8)
        combined_mask = Image.fromarray(combined_mask)

        img_dir = ""
        if args.bindings:
            image_name = bindings_dict[id].split('.')[0]
            img_dir = os.path.join(save_dir, f'{image_name}{args.suffix}.png')
        else:
            img_dir = os.path.join(save_dir, f'{id}{args.suffix}.png')

        combined_mask.save(img_dir)
        print(f'Combined mask from annotation {id} saved to {img_dir}')