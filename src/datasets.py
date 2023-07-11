import torch
import cv2
import numpy as np
import os
import glob as glob
from xml.etree import ElementTree as et
from config import CLASSES, RESIZE_TO, TRAIN_JSON, VALID_JSON, IMAGES_DIR, BATCH_SIZE
from torch.utils.data import Dataset, DataLoader
from utils import collate_fn, get_train_transform, get_valid_transform
import json

class InteriorDataset(Dataset):
    def __init__(self, images_dir_path, annotations_json, width, height, classes, transforms=None):
        self.transforms = transforms
        self.images_dir_path = images_dir_path
        self.height = height
        self.width = width
        self.classes = classes
        self.image_paths = []
        
        with open(annotations_json, encoding='utf-8') as json_file:
            self.annotations = json.load(json_file)

        for image in self.annotations['images']:
            self.image_paths.append(f"{self.images_dir_path}\\{image['file_name']}")

        self.all_images = [image_path.split('\\')[-1] for image_path in self.image_paths]
        self.all_images = sorted(self.all_images)
    
    def __getitem__(self, idx):

        image_name = self.all_images[idx]
        image_path = os.path.join(self.images_dir_path, image_name)
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float32)
        image_resized = cv2.resize(image, (self.width, self.height))
        image_resized /= 255.0
                
        boxes = []
        labels = []
        img_id = 0
        
        image_width = image.shape[1]
        image_height = image.shape[0]
        
        for img in self.annotations['images']:
            if image_name == img["file_name"]:
                img_id = img["id"]
                break
        for annot in self.annotations['annotations']:
            if img_id == 0 or img_id != annot['image_id']:
                continue

            labels.append(annot['category_id'])
            xmin = int(annot['bbox'][0])
            xmax = int(annot['bbox'][0]+annot['bbox'][2])
            ymin = int(annot['bbox'][1])
            ymax = int(annot['bbox'][1]+annot['bbox'][3])
            
            xmin_final = (xmin/image_width)*self.width
            xmax_final = (xmax/image_width)*self.width
            ymin_final = (ymin/image_height)*self.height
            ymax_final = (ymax/image_height)*self.height
            
            boxes.append([xmin_final, ymin_final, xmax_final, ymax_final])
        
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        iscrowd = torch.zeros((boxes.shape[0],), dtype=torch.int64)
        labels = torch.as_tensor(labels, dtype=torch.int64)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["area"] = area
        target["iscrowd"] = iscrowd
        image_id = torch.tensor([idx])
        target["image_id"] = image_id

        if self.transforms:
            sample = self.transforms(image = image_resized,
                                     bboxes = target['boxes'],
                                     labels = labels)
            image_resized = sample['image']
            target['boxes'] = torch.Tensor(sample['bboxes'])
            
        return image_resized, target
    
    def __len__(self):
        return len(self.all_images)
    
train_dataset = InteriorDataset(IMAGES_DIR, TRAIN_JSON, RESIZE_TO, RESIZE_TO, CLASSES, get_train_transform())
valid_dataset = InteriorDataset(IMAGES_DIR, VALID_JSON, RESIZE_TO, RESIZE_TO, CLASSES, get_valid_transform())
train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0,
    collate_fn=collate_fn
)
valid_loader = DataLoader(
    valid_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0,
    collate_fn=collate_fn
)
print(f"Number of training samples: {len(train_dataset)}")
print(f"Number of validation samples: {len(valid_dataset)}\n")

if __name__ == '__main__':

    dataset = InteriorDataset(
        IMAGES_DIR, TRAIN_JSON, 
        RESIZE_TO, RESIZE_TO, CLASSES
    )
    print(f"Number of training images: {len(dataset)}")
    
    def visualize_sample(image, target):
        box = target['boxes'][0]
        label = CLASSES[target['labels'][0]]
        cv2.rectangle(
            image, 
            (int(box[0]), int(box[1])), (int(box[2]), int(box[3])),
            (0, 255, 0), 1
        )
        cv2.putText(
            image, label, (int(box[0]), int(box[1]-5)), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2
        )
        cv2.imshow('Image', image)
        cv2.waitKey(0)
        
    NUM_SAMPLES_TO_VISUALIZE = 5
    for i in range(NUM_SAMPLES_TO_VISUALIZE):
        image, target = dataset[i]
        visualize_sample(image, target)