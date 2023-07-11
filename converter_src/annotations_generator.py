import copy
import cv2
import os
import json
from datetime import datetime
from converter_src.progressbar import progressbar
import shutil

def add_annotations(dataset_path, json_train, json_test, json_val, dataset_id, classes, path):

    annot_id = dataset_id

    files = os.listdir(dataset_path)
    
    print('Converting annotation files...')
    image_counter = 0
    for filenum, file in enumerate(files):
        filepath = os.path.join(dataset_path, file)
            
        if os.path.isfile(filepath) and filepath[-4:].find('png') != -1:

            image_counter += 1

            if (image_counter/(len(files)/2) < 0.7):
                json_data = json_train
            elif (image_counter/(len(files)/2) > 0.85):
                json_data = json_test
            else:
                json_data = json_val

            image = {
                "license": 0,
                "flickr_url": "none",
                "coco_url": "none"
            }
            
            with open(os.path.join(dataset_path, f"0{file[1:-3]}") + 'json', encoding='utf-8') as json_file:
                json_text = json.load(json_file)
            
            img = cv2.imread(f'{filepath}')
            h, w, c = img.shape
            image["date_captured"] = str(datetime.fromtimestamp(os.path.getctime(filepath)))
            image["file_name"] = str(dataset_id + int(file[1:-4])) + ".png"
            image["width"] = w
            image["height"] = h
            image["id"] = dataset_id + int(file[1:-4])

            for object in json_text["objects"]:

                if object["visibility"] < 0.2 or \
                    any(coord < 0 for coord in object["bounding_box"]["top_left"]):
                        continue
                
                if object["bounding_box"]["bottom_right"][0] > w:
                    object["bounding_box"]["bottom_right"][0] = w
                if object["bounding_box"]["bottom_right"][1] > h:
                    object["bounding_box"]["bottom_right"][1] = h

                if object["bounding_box"]["bottom_right"][0] <= object["bounding_box"]["top_left"][0]:
                        continue
                if object["bounding_box"]["bottom_right"][1] <= object["bounding_box"]["top_left"][1]:
                    continue

                annot_id += 1

                bbox_w = object["bounding_box"]["bottom_right"][1] - object["bounding_box"]["top_left"][1]
                bbox_h = object["bounding_box"]["bottom_right"][0] - object["bounding_box"]["top_left"][0]

                annotation = {
                    "id": annot_id,
                    "image_id": image["id"],
                    "category_id": classes[object['class']],
                    "segmentation": [
                        object["bounding_box"]["top_left"][1],
                        object["bounding_box"]["top_left"][0],
                        object["bounding_box"]["top_left"][1],
                        object["bounding_box"]["top_left"][0] + bbox_h,
                        object["bounding_box"]["top_left"][1] + bbox_w,
                        object["bounding_box"]["top_left"][0] + bbox_h,
                        object["bounding_box"]["top_left"][1] + bbox_w,
                        object["bounding_box"]["top_left"][0],
                    ],
                    "area": bbox_w * bbox_h,
                    "bbox": [
                        object["bounding_box"]["top_left"][1],
                        object["bounding_box"]["top_left"][0],
                        bbox_w,
                        bbox_h,
                    ],
                    "iscrowd": 0
                }
                json_data["annotations"].append(annotation)
                
            if not json_data["annotations"]:
                continue
                
            json_data["images"].append(image)

            shutil.copy(filepath, f"{path}\\images\\{image['file_name']}")

        progressbar(len(files), filenum+1)
    print()

    return json_train, json_test, json_val
            
def generate_annotation(dataset_path, path):
    
    if not os.path.exists(f"{path}\\images"):
        print('Does not exist')
        os.makedirs(f'{path}\\images')
    if not os.path.exists(f"{path}\\annotations"):
        os.makedirs(f'{path}\\annotations')

    json_data = {
        "info": {
            "year": 2023,
            "version": "1.0",
            "description": "Synthetic interiors dataset using UE4",
            "contributor": "Temnyy Daniil",
            "url": "https://disk.yandex.ru/d/_icieU6dtNPqnw",
            "date_created": "2023/07/07"
        },
        "images": [],
        "annotations": [],
        "licenses": [
            {
                "id": 0,
                "name": "-",
                "url": "-"
            }
        ]
    }

    classes = sorted([ 
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

    classes_ids = {}
    for i, item in enumerate(classes):
        classes_ids[item] = i+1

    json_data["categories"] = []

    for key in sorted(classes_ids):
        json_data["categories"].append({
            "supercategory": "none",
            "id": classes_ids[key],
            "name": key
        })

    json_train = copy.deepcopy(json_data)
    json_test = copy.deepcopy(json_data)
    json_val = copy.deepcopy(json_data)

    for i, folder in enumerate(os.listdir(dataset_path)):
        print(f'Converting {folder} folder...')
        folder_path = os.path.join(dataset_path, folder)
        json_train, json_test, json_val = add_annotations(folder_path, json_train, json_test, json_val, 100000 * (i + 1), classes_ids, path)

    return json_train, json_test, json_val


if __name__ == '__main__':

    path = os.getcwd()
    dataset_path = path[:path.rindex('\\')] + "\\dataset_output\\"

    json_train, json_test, json_val = generate_annotation(dataset_path, path)
    
    with open(f'{path}\\dataset\\annotations\\train.json', "w", encoding='utf-8') as json_file:
        json.dump(json_train, json_file, indent=4)
    with open(f'{path}\\dataset\\annotations\\test.json', "w", encoding='utf-8') as json_file:
        json.dump(json_test, json_file, indent=4)
    with open(f'{path}\\dataset\\annotations\\val.json', "w", encoding='utf-8') as json_file:
        json.dump(json_val, json_file, indent=4)
