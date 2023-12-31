import numpy as np
import cv2
import torch
import glob as glob
from model import create_model
import os

path = os.getcwd()
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

CLASSES = ['background'] + sorted([
    "shelf",
    "lamp",
    "coffeetable",
    "chair",
    "stool",
    "sofa",
    "bed",
    "coathanger",
    "plant",
    "tv",
    "sidetable",
    "table",
    "toilet",
    "bathtub"
    ])

model = create_model(num_classes=len(CLASSES)).to(device)
model.load_state_dict(torch.load(
    f'{path}\\outputs\\model100.pth', map_location=device
))
model.eval()

DIR_TEST = f'{path}\\dataset\\test_data'
test_images = glob.glob(f"{DIR_TEST}\\*")
print(f"Test instances: {len(test_images)}")


detection_threshold = 0.8

for i in range(len(test_images)):

    image_name = test_images[i].split('\\')[-1].split('.')[0]
    image = cv2.imread(test_images[i])
    orig_image = image.copy()

    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB).astype(np.float32)

    image /= 255.0

    image = np.transpose(image, (2, 0, 1)).astype(np.float64)

    image = torch.tensor(image, dtype=torch.float).cuda() if torch.cuda.is_available() else torch.tensor(image, dtype=torch.float)

    image = torch.unsqueeze(image, 0)
    with torch.no_grad():
        outputs = model(image)
    
    outputs = [{k: v.to('cpu') for k, v in t.items()} for t in outputs]

    if len(outputs[0]['boxes']) != 0:
        boxes = outputs[0]['boxes'].data.numpy()
        scores = outputs[0]['scores'].data.numpy()

        boxes = boxes[scores >= detection_threshold].astype(np.int32)
        draw_boxes = boxes.copy()

        pred_classes = [CLASSES[i] for i in outputs[0]['labels'].cpu().numpy()]
        
        for j, box in enumerate(draw_boxes):
            cv2.rectangle(orig_image,
                        (int(box[0]), int(box[1])),
                        (int(box[2]), int(box[3])),
                        (0, 0, 255), 2)
            cv2.putText(orig_image, pred_classes[j], 
                        (int(box[0]), int(box[1]-5)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 
                        2, lineType=cv2.LINE_AA)
        cv2.imshow('Prediction', orig_image)
        cv2.waitKey(1)
        cv2.imwrite(f"{path}\\test_predictions\\{image_name}.png", orig_image,)
    print(f"Image {i+1} done...")
    print('-'*50)
print('TEST PREDICTIONS COMPLETE')
cv2.destroyAllWindows()