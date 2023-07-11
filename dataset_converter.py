from converter_src.annotations_generator import generate_annotation
from converter_src.class_converter import convert
import os
import json
import argparse

if __name__ == '__main__':
        
    path = os.getcwd()

    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", metavar="PATH", default=path[:path.rindex('\\')] + "\\dataset_output\\",
        help="path to input dataset folder")
    ap.add_argument("-o", "--output", metavar="PATH", default=f'{path}\\dataset',
        help="path to output folder for dataset")
    args = vars(ap.parse_args())

    dataset_path = args['input']

    output_path = args['output']

    convert(dataset_path)

    json_train, json_test, json_val = generate_annotation(dataset_path, output_path)
    
    with open(f'{output_path}\\annotations\\train.json', "w", encoding='utf-8') as json_file:
        json.dump(json_train, json_file, indent=4)
    with open(f'{output_path}\\annotations\\test.json', "w", encoding='utf-8') as json_file:
        json.dump(json_test, json_file, indent=4)
    with open(f'{output_path}\\annotations\\val.json', "w", encoding='utf-8') as json_file:
        json.dump(json_val, json_file, indent=4)
