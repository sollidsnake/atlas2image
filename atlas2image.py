#!/usr/bin/python3

import os
import argparse
from PIL import Image

class Atlas2Image:
    img_path: str
    width: int
    height: int
    name_swap_xy = False

    def __init__(self, img_path, width, height, name_x=[], name_y=[]):
        self.img_path = img_path
        self.width = width
        self.height = height
        self.name_x = name_x
        self.name_y = name_y

    @staticmethod
    def _get_name(names, index):
        if index < len(names):
            return names[index]
        return index

    def _crop(self):
        img: PIL.PngImagePlugin.PngImageFile = Image.open(self.img_path)
        total_width, total_height = img.size

        if total_width % self.width or total_height % self.height:
            raise ValueError("Cropped width or height doesn't match image size")

        x_frames = int(total_width / self.width)
        y_frames = int(total_height / self.height)

        imgs = []
        for xf in range(x_frames):
            for yf in range(y_frames):
                x_init = self.width * xf
                y_init = self.height * yf
                x_end = x_init + self.width
                y_end = y_init + self.height

                name_x = self._get_name(self.name_x, xf)
                name_y = self._get_name(self.name_y, yf)

                if self.name_swap_xy:
                    name_x, name_y = name_y, name_x

                imgs.append({
                    'pos': '%s-%s' % (
                        name_x,
                        name_y,
                    ),
                    'img': img.crop((x_init, y_init, x_end, y_end))
                })

        for img in imgs:
            yield img

    def crop(self):
        self.imgs = self._crop()

    def save_img(self, dest_dir=None):
        if dest_dir is None:
            dest_dir = '.'

        for img in self.imgs:
            img['img'].save(os.path.join(dest_dir, img['pos']) + '.png', 'PNG')


    @staticmethod
    def process_name(name=None):
        if type(name) != str:
            return []

        names = []
        for i in name.split(','):
            names.append(i.strip())

        return names


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crop atlas images')
    parser.add_argument('img_path', type=str)
    parser.add_argument('width', type=int)
    parser.add_argument('height', type=int)
    parser.add_argument('--output-path', type=str)
    parser.add_argument('--name-x', type=str)
    parser.add_argument('--name-y', type=str)
    parser.add_argument('--name-swap-xy', action='store_true', dest='name_swap')

    arg = parser.parse_args()

    name_x = (Atlas2Image.process_name(arg.name_x))
    name_y = (Atlas2Image.process_name(arg.name_y))

    atlas = Atlas2Image(arg.img_path, arg.width, arg.height, name_x=name_x, name_y=name_y)
    atlas.name_swap_xy = arg.name_swap
    atlas.crop()
    atlas.save_img(arg.output_path)
