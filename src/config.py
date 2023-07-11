import torch
import os

CWD = os.getcwd()
BATCH_SIZE = 4
RESIZE_TO = 512
NUM_EPOCHS = 100
DEVICE = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

TRAIN_JSON = CWD + '\\dataset\\annotations\\train.json'
VALID_JSON = CWD + '\\dataset\\annotations\\val.json'
IMAGES_DIR = CWD + '\\dataset\\images'

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
NUM_CLASSES = len(CLASSES)

VISUALIZE_TRANSFORMED_IMAGES = False

OUT_DIR = CWD + '\\outputs'
SAVE_PLOTS_EPOCH = 10 # save loss plots after these many epochs
SAVE_MODEL_EPOCH = 5 # save model after these many epochs