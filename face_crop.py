# -*- coding: utf-8 -*-
import commandr
import os
from PIL import Image
from file_manager import FileManager


class FaceLocLoader(object):
    def __init__(self, dir_name):
        self.dir_name = dir_name

    def load(self, key):
        filename = os.path.join(self.dir_name, '{}.csv'.format(key))
        with open(filename, 'r') as file_obj:
            for line in file_obj:
                line = line.strip()
                if line == '':
                    continue
                parts = line.split(',')

                loc = map(int, parts[1:])
                img_filename = parts[0]
                idx = int(img_filename.rsplit('/', 1)[-1].split('.')[0])

                yield img_filename, idx, loc


@commandr.command('crop')
def crop(input_dir='/home/lxh12/face_loc', out_dir='/home/lxh/face_frames'):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    loader = FaceLocLoader(dir_name=input_dir)

    for mode, lang in FileManager.mode_lang:
        for key in FileManager.get_keys(mode, lang):
            sub_out_dir = os.path.join(out_dir, key)
            if not os.path.exists(sub_out_dir):
                os.mkdir(sub_out_dir)

            items = list(loader.load(key))
            for img_filename, idx, loc in items:
                out_file = os.path.join(sub_out_dir, '{}.png'.format(idx))
                Image.open(img_filename).crop(loc).reshape([100, 100]).save(out_file)


if __name__ == '__main__':
    commandr.Run()
