# -*- coding: utf-8 -*-
import math
import os
import shutil
from file_manager import FileManager


d_face_frames = '/home/lxh12/face_frames'


def get_ref_n(key):
    f = open('/home/lxh12/AVEC2018_CES/visual_features/{}.csv'.format(key), 'r')
    lines = f.read().strip().split('\n')
    return int(math.ceil(float(len(lines)) / 5))


def filename_face(key, idx):
    return '/home/lxh12/face_frames/{}/{}.png'.format(key, idx)


def main():
    for mode, lang in FileManager.mode_lang:
        for key in FileManager.get_keys(mode, lang):
            print(key)
            ref_n = get_ref_n(key)
            f_exists = {idx: os.path.exists(filename_face(key, idx)) for idx in range(1, ref_n + 1)}

            for idx in range(1, ref_n + 1):
                if not f_exists[idx]:
                    for j in range(1, ref_n + 1):
                        if f_exists.get(idx + j, False) is True:
                            shutil.copy(filename_face(key, idx + j), filename_face(key, idx))
                            break
                        if f_exists.get(idx - j, False) is True:
                            shutil.copy(filename_face(key, idx - j), filename_face(key, idx))
                            break


if __name__ == '__main__':
    main()
