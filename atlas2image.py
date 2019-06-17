from PIL import Image
import argparse

def crop(image_path, width, height):
    img: PIL.PngImagePlugin.PngImageFile = Image.open(image_path)
    total_width, total_height = img.size

    if total_width % width or total_height % height:
        raise ValueError("Cropped width or height doesn't match image size")

    x_frames = int(total_width / width)
    y_frames = int(total_height / height)

    imgs = []
    for xf in range(x_frames):
        for yf in range(y_frames):
            x_init = width * xf
            y_init = height * yf
            x_end = x_init + width
            y_end = y_init + height
            imgs.append(
                {
                    'pos': '%s-%s' % (xf, yf),
                    'img': img.crop((x_init, y_init, x_end, y_end))
                }
            )

    for img in imgs:
        img['img'].save(img['pos'] + '.png', 'PNG')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crop atlas images')
    parser.add_argument('img_path', type=str)
    parser.add_argument('width', type=int)
    parser.add_argument('height', type=int)
    arg = parser.parse_args()
    crop(arg.img_path, arg.width, arg.height)
