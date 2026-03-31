import os
import shutil
import random

IMAGE_DIR = "../data/processed/images"
ANNO_DIR = "../data/processed/annos"

OUTPUT_DIR = "../data/split"

train_ratio = 0.7
val_ratio = 0.15
test_ratio = 0.15

images = os.listdir(IMAGE_DIR)

random.shuffle(images)

total = len(images)

train_end = int(train_ratio * total)
val_end = train_end + int(val_ratio * total)

train_files = images[:train_end]
val_files = images[train_end:val_end]
test_files = images[val_end:]

print("Train:", len(train_files))
print("Val:", len(val_files))
print("Test:", len(test_files))


def copy_files(file_list, split):

    img_out = os.path.join(OUTPUT_DIR, split, "images")
    ann_out = os.path.join(OUTPUT_DIR, split, "annos")

    os.makedirs(img_out, exist_ok=True)
    os.makedirs(ann_out, exist_ok=True)

    for img in file_list:

        anno = img.replace(".jpg", ".json")

        src_img = os.path.join(IMAGE_DIR, img)
        dst_img = os.path.join(img_out, img)

        src_ann = os.path.join(ANNO_DIR, anno)
        dst_ann = os.path.join(ann_out, anno)

        shutil.copy(src_img, dst_img)
        shutil.copy(src_ann, dst_ann)


copy_files(train_files, "train")
copy_files(val_files, "val")
copy_files(test_files, "test")

print("Dataset split completed")
