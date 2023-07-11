from converter_src.annotations_generator import generate_annotation
from converter_src.class_converter import convert
import os
import json
import argparse

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", required=True, metavar="PATH",
        help="path to input dataset folder")
    ap.add_argument("-o", "--output", required=True, metavar="PATH",
        help="path to output dataset folder")
    args = vars(ap.parse_args())

    if not args[0]:
        path = os.getcwd()
        dataset_path = path[:path.rindex('\\')] + "\\dataset_output\\"
    else:
        dataset_path = args[0]

    if not args[1]:
        output_path = f'{path}\\dataset'
    else:
        output_path = args[1]

    convert(dataset_path)

    json_train, json_test, json_val = generate_annotation(dataset_path, path)
    
    with open(f'{output_path}\\annotations\\train.json', "w", encoding='utf-8') as json_file:
        json.dump(json_train, json_file, indent=4)
    with open(f'{output_path}\\annotations\\test.json', "w", encoding='utf-8') as json_file:
        json.dump(json_test, json_file, indent=4)
    with open(f'{output_path}\\annotations\\val.json', "w", encoding='utf-8') as json_file:
        json.dump(json_val, json_file, indent=4)
