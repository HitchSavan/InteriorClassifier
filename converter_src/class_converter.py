import json
import os
from progressbar import progressbar

def change_instance(dataset_path, change_inst):
    files = os.listdir(dataset_path)
    for iter, file in enumerate(files):
        filepath = os.path.join(dataset_path, file)
        if os.path.isfile(filepath) and filepath.find('json') != -1:
            with open(filepath, encoding='utf-8') as json_file:
                json_text = json.dumps(json.load(json_file))
            for key in change_inst:
                json_text = json_text.replace(key, change_inst[key])
            with open(filepath, "w", encoding='utf-8') as json_file:
                json.dump(json.loads(json_text), json_file, indent=4)
        progressbar(len(files), iter+1)

def convert_folder(dataset_path, classes):

    change_inst = {}

    with open(f"{dataset_path}\\_object_settings.json", encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    print("Changing class names...")
    for iter, item in enumerate(json_data["exported_object_classes"]):
        match = False
        for inst in classes:
            if item.lower().find(inst) != -1:
                match = True
                if inst == "shelv" or inst == "cabinet":
                    change_inst[item] = "shelf"
                elif inst == "couch":
                    change_inst[item] = "sofa"
                elif inst == "commode" or inst == "cupboard" or inst == "wardrobe":
                    change_inst[item] = "sidetable"
                else:
                    change_inst[item] = inst
                break
        if not match:
            inst = input(f"Could not find matchig class for {item}, please specify: ")
            change_inst[item] = inst

    print("Converting class names in annotations...")
    files = os.listdir(dataset_path)
    change_instance(dataset_path, change_inst)
    print()

    change_inst = {}
    need_rerun = False
    
    print("Validating classes...")
    with open(f"{dataset_path}\\_object_settings.json", encoding='utf-8') as json_file:
        json_data = json.load(json_file)
    for iter, item in enumerate(json_data["exported_object_classes"]):
        match = False
        for inst in classes:
            if item.lower() == inst:
                match = True
                break
        if not match:

            inst = input(f"Could not validate class for {item}, please specify: ")
            
            change_inst[item] = inst
            need_rerun = True

    if need_rerun:
        print("Re-converting class names in annotations...")
        change_instance(dataset_path, change_inst)
        print()
    else:
        print("OK")


def convert(dataset_path):
    
    classes = [
        "shelf",
        "shelv",
        "lamp",
        "coffeetable",
        "chair",
        "stool",
        "couch",
        "sofa",
        "bed",
        "coathanger",
        "plant",
        "tv",
        "sidetable",
        "table",
        "toilet",
        "bathtub",
        "commode",
        "cupboard",
        "cabinet",
        "wardrobe"
    ]

    for folder in os.listdir(dataset_path):
        print(f'Converting {folder} folder...')
        folder_path = os.path.join(dataset_path, folder)
        convert_folder(folder_path, classes)


if __name__ == '__main__':

    path = os.getcwd()
    dataset_path = path[:path.rindex('\\')] + "\\dataset_output\\"

    convert(dataset_path)