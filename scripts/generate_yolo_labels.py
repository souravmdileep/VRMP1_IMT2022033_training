import os
import json
import cv2

DATASET_DIR = "../data/split"

CLASS_MAP = {
    1:0,
    8:1,
    7:2,
    2:3,
    9:4
}

def convert_box(img_w,img_h,x1,y1,x2,y2):

    w = x2-x1
    h = y2-y1

    xc = x1 + w/2
    yc = y1 + h/2

    return (
        xc/img_w,
        yc/img_h,
        w/img_w,
        h/img_h
    )


def process_split(split):

    image_dir = os.path.join(DATASET_DIR,split,"images")
    anno_dir = os.path.join(DATASET_DIR,split,"annos")
    label_dir = os.path.join(DATASET_DIR,split,"labels")

    os.makedirs(label_dir,exist_ok=True)

    images = os.listdir(image_dir)

    for img_file in images:

        img_path = os.path.join(image_dir,img_file)
        anno_file = img_file.replace(".jpg",".json")
        anno_path = os.path.join(anno_dir,anno_file)

        img = cv2.imread(img_path)
        h,w,_ = img.shape

        with open(anno_path) as f:
            data = json.load(f)

        label_path = os.path.join(label_dir,img_file.replace(".jpg",".txt"))

        with open(label_path,"w") as out:

            for key in data:

                if key.startswith("item"):

                    cat = data[key]["category_id"]

                    if cat not in CLASS_MAP:
                        continue

                    x1,y1,x2,y2 = data[key]["bounding_box"]

                    xc,yc,box_w,box_h = convert_box(w,h,x1,y1,x2,y2)

                    out.write(
                        f"{CLASS_MAP[cat]} {xc} {yc} {box_w} {box_h}\n"
                    )


for split in ["train","val","test"]:

    print("Processing",split)
    process_split(split)

print("YOLO labels generated")
