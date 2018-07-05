# -*- coding: utf-8 -*-
from __future__ import print_function
import commandr
import os
import time
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
def crop(mode, lang, input_dir='/home/lxh12/face_loc', out_dir='/home/lxh12/face_frames_ori'):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    loader = FaceLocLoader(dir_name=input_dir)

    for key in FileManager.get_keys(mode, lang):
        print(key, end='')
        st = time.time()

        sub_out_dir = os.path.join(out_dir, key)
        if not os.path.exists(sub_out_dir):
            os.mkdir(sub_out_dir)

        items = list(loader.load(key))
        for img_filename, idx, loc in items:
            a, b, c, d = loc
            if a > c:
                a, c = c, a
            if b > d:
                b, d = d, b

            width = c - a + 1
            height = d - b + 1
            if width > height:
                d = int(float(width) / 2 + float(d + b) / 2)
                b = d - width + 1
                if b < 0:
                    d -= b
                    b = 0
            elif height > width:
                c = int(float(height) / 2 + float(a + c) / 2)
                a = c - height + 1
                if a < 0:
                    c -= a
                    a = 0

            loc = [b, a, d, c]
            out_file = os.path.join(sub_out_dir, '{}.png'.format(idx))
            Image.open(img_filename).crop(loc).resize([100, 100]).save(out_file)

        et = time.time()
        print(' - {} sec'.format(et - st))


if __name__ == '__main__':
    commandr.Run()
