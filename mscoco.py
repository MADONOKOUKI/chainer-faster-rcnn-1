import os
import cv2
import numpy as np
import psutil
import profiler
import json


def _filename_from_id(id, group='train'):
    if isinstance(id, int):
        id = str(id)
    padding = '0' * (12 - len(id))
    return 'COCO_{}2014_{}.jpg'.format(group, padding + id)


class MSCOCO:

    def __init__(self):
        self.files = {}
        self.annotations = {}

    def load_annotations(self, path):
        with open(path) as jsonfile:
            decoded = json.load(jsonfile)
            for annotation in decoded['annotations']:
                filename = _filename_from_id(annotation['image_id'])
                if filename in self.annotations:
                    self.annotations[filename].append(annotation)
                else:
                    self.annotations[filename] = []
                print(self.annotations[filename])

    def load_images(self, path):
        for f in os.listdir(path):
            if os.path.isfile(os.path.join(path, f)):
                self.files[f] = cv2.imread(os.path.join(path, f))
                print('Loaded image with shape {}'.format(self.files[f].shape))  # In the order, height, width, channels

    def _load_images(self, path):
        """
        Use later. Not used at the moment since we want to use dictionaries and not lists.
        """
        self.files = [f for f in os.listdir(self.target_dir) if os.path.isfile(os.path.join(self.target_dir, f))]
        for file in files:
            train.append(cv2.imread(os.path.join(self.target_dir, file)))
        train = np.array(train).astype(np.float32).reshape((len(train), self.num_channels, self.width, self.height)) / 255


    def image(self, id, group='train'):
        filename = _filename_from_id(id, group)
        image = self.files[filename]
        height, width, channels = image.shape
        image = np.array([image]).astype(np.float32).reshape((1, channels, width, height)) / 255
        annotation = self.annotations[filename]
        return image, annotation


if __name__ == '__main__':
    print('Memory usage (before): {} MB'.format(profiler.memory_usage(format='mb')))
    coco = MSCOCO()
    print('Loading images...')
    coco.load_images('./data/coco/images/test')
    print('Done loading images')
    print('Loading annotations...')
    coco.load_annotations('./data/coco/annotations/233833_annotations.json')
    print('Done loading annotations')
    print('Memory usage (after): {} MB'.format(profiler.memory_usage(format='mb')))
    image, ann = coco.image('233833')
    print(image.shape)
    print(ann)
