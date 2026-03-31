import os
import json
from collections import Counter
from tqdm import tqdm

ANNOTATION_DIR = "../data/raw/train/annos"

category_counter = Counter()

files = os.listdir(ANNOTATION_DIR)

print("Total annotation files:", len(files))

for file in tqdm(files):

    path = os.path.join(ANNOTATION_DIR, file)

    with open(path, "r") as f:
        data = json.load(f)

    # iterate through annotation keys
    for key in data:

        # we only care about clothing items
        if key.startswith("item"):

            item = data[key]

            if "category_id" in item:
                category_id = item["category_id"]
                category_counter[category_id] += 1


print("\nCategory frequency:\n")

for k, v in sorted(category_counter.items()):
    print(f"Category {k}: {v}")

print("\nTop 5 categories:\n")

top5 = category_counter.most_common(5)

for cat, count in top5:
    print(f"Category {cat}: {count}")