import os
import json
import cv2
import numpy as np

DATASET_DIR = "../data/split"

CLASS_MAP = {
    1:0,  # short sleeve top
    8:1,  # trousers
    7:2,  # shorts
    2:3,  # long sleeve top
    9:4   # skirt
}


def process_split(split):

    image_dir = os.path.join(DATASET_DIR,split,"images")
    anno_dir = os.path.join(DATASET_DIR,split,"annos")
    mask_dir = os.path.join(DATASET_DIR,split,"masks")

    os.makedirs(mask_dir,exist_ok=True)

    images = os.listdir(image_dir)

    for img_file in images:

        img_path = os.path.join(image_dir,img_file)
        anno_file = img_file.replace(".jpg",".json")
        anno_path = os.path.join(anno_dir,anno_file)

        img = cv2.imread(img_path)
        h,w,_ = img.shape

        mask = np.zeros((h,w),dtype=np.uint8)

        with open(anno_path) as f:
            data = json.load(f)

        for key in data:

            if key.startswith("item"):

                cat = data[key]["category_id"]

                if cat not in CLASS_MAP:
                    continue

                cls = CLASS_MAP[cat] + 1

                seg = data[key]["segmentation"]

                if len(seg) == 0:
                    continue

                polygon = np.array(seg[0]).reshape(-1,2).astype(np.int32)

                cv2.fillPoly(mask,[polygon],cls)

        mask_path = os.path.join(mask_dir,img_file.replace(".jpg",".png"))
        cv2.imwrite(mask_path,mask)


for split in ["train","val","test"]:

    print("Processing",split)
    process_split(split)

print("Segmentation masks generated")
