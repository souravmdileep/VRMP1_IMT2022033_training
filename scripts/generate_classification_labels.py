import os
import json
import csv

DATASET_DIR = "../data/split"

# original → remapped labels
CLASS_MAP = {
    1:0,
    8:1,
    7:2,
    2:3,
    9:4
}

NUM_CLASSES = 5


def generate_labels(split):

    image_dir = os.path.join(DATASET_DIR, split, "images")
    anno_dir = os.path.join(DATASET_DIR, split, "annos")

    images = os.listdir(image_dir)

    output_file = os.path.join(DATASET_DIR, split, "labels.csv")

    with open(output_file,"w",newline="") as f:

        writer = csv.writer(f)

        header = ["image"] + [f"class_{i}" for i in range(NUM_CLASSES)]
        writer.writerow(header)

        for img in images:

            anno_file = img.replace(".jpg",".json")
            anno_path = os.path.join(anno_dir,anno_file)

            label = [0]*NUM_CLASSES

            with open(anno_path,"r") as jf:
                data = json.load(jf)

            for key in data:

                if key.startswith("item"):

                    cat = data[key]["category_id"]

                    if cat in CLASS_MAP:
                        label[CLASS_MAP[cat]] = 1

            writer.writerow([img] + label)


for split in ["train","val","test"]:

    print("Processing:",split)
    generate_labels(split)

print("Classification labels generated")
