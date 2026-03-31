import os
import json
import cv2
import random

IMAGE_DIR = "../data/processed/images"
ANNO_DIR = "../data/processed/annos"

# category mapping
CATEGORY_MAP = {
    1: "short sleeve top",
    2: "long sleeve top",
    3: "short sleeve outwear",
    4: "long sleeve outwear",
    5: "vest",
    6: "sling",
    7: "shorts",
    8: "trousers",
    9: "skirt",
    10: "short sleeve dress",
    11: "long sleeve dress",
    12: "vest dress",
    13: "sling dress"
}

files = os.listdir(ANNO_DIR)

sample_files = random.sample(files, 10)

for file in sample_files:

    anno_path = os.path.join(ANNO_DIR, file)
    img_path = os.path.join(IMAGE_DIR, file.replace(".json",".jpg"))

    img = cv2.imread(img_path)

    with open(anno_path,"r") as f:
        data = json.load(f)

    for key in data:

        if key.startswith("item"):

            item = data[key]

            cat_id = item["category_id"]
            label = CATEGORY_MAP.get(cat_id,"unknown")

            x1,y1,x2,y2 = item["bounding_box"]

            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)

            cv2.putText(
                img,
                label,
                (x1, y1-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0,255,0),
                1
            )

    cv2.imshow("Dataset Visualization",img)
    cv2.waitKey(0)

cv2.destroyAllWindows()