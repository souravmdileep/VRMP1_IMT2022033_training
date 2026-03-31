import os
import json
import shutil
import random
from tqdm import tqdm

IMAGE_DIR = "../data/raw/train/image"
ANNO_DIR = "../data/raw/train/annos"

OUTPUT_IMAGE_DIR = "../data/processed/images"
OUTPUT_ANNO_DIR = "../data/processed/annos"

TOP5 = {1,2,7,8,9}

TARGET_IMAGES = 20000

valid_files = []

files = os.listdir(ANNO_DIR)

print("Scanning full dataset...")

for file in tqdm(files):

    path = os.path.join(ANNO_DIR, file)

    with open(path,"r") as f:
        data = json.load(f)

    for key in data:

        if key.startswith("item"):

            if data[key]["category_id"] in TOP5:
                valid_files.append(file)
                break


print("Total candidate images:", len(valid_files))

print("Random sampling...")

sample_files = random.sample(valid_files, TARGET_IMAGES)

print("Copying dataset...")

for file in tqdm(sample_files):

    image_file = file.replace(".json",".jpg")

    src_img = os.path.join(IMAGE_DIR,image_file)
    dst_img = os.path.join(OUTPUT_IMAGE_DIR,image_file)

    src_anno = os.path.join(ANNO_DIR,file)
    dst_anno = os.path.join(OUTPUT_ANNO_DIR,file)

    shutil.copy(src_img,dst_img)
    shutil.copy(src_anno,dst_anno)

print("\nDataset created successfully")
print("Total images:",len(sample_files))
