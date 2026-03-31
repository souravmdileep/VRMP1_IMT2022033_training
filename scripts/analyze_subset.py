import os
import json
from collections import Counter
from tqdm import tqdm

ANNO_DIR = "../data/processed/annos"

counter = Counter()

files = os.listdir(ANNO_DIR)

print("Total files:", len(files))

for file in tqdm(files):

    path = os.path.join(ANNO_DIR, file)

    with open(path, "r") as f:
        data = json.load(f)

    for key in data:

        if key.startswith("item"):

            cat = data[key]["category_id"]
            counter[cat] += 1

print("\nSubset distribution:\n")

for k, v in sorted(counter.items()):
    print(k, v)
