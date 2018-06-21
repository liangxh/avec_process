# -*- coding: utf-8 -*-
import os
import commandr
from file_manager import FileManager
from csv_loader import CSVLoader
import math
from sklearn import preprocessing
from sampling import Sampler


DEFAULT_VALUE = -9999.
SAMPLE_RATE = 10

dir_output = '/home/lxh12/AVEC2018_data'
dir_root = '/home/lxh12/AVEC2018_CES'
dir_labels = os.path.join(dir_root, 'labels')


def get_batch_from_video(video, batch_size, batch_idx, dim):
    vec_list, label_list = video
    partial_vec_list = vec_list[(batch_idx * batch_size): ((batch_idx + 1) * batch_size)]
    partial_label_list = label_list[(batch_idx * batch_size): ((batch_idx + 1) * batch_size)]
    seq_len = len(partial_vec_list)

    if seq_len < batch_size:
        diff_len = batch_size - seq_len
        partial_vec_list += [[DEFAULT_VALUE] * dim] * diff_len
        partial_label_list += [[DEFAULT_VALUE] * 3] * diff_len

    return partial_vec_list, partial_label_list, seq_len


@commandr.command('pack')
def pack(input_dirname, batch_size):
    batch_size = int(batch_size)
    input_dirname = os.path.join(dir_root, input_dirname)

    scaler = preprocessing.StandardScaler()
    vec_list = list()
    for key in FileManager.get_keys('train'):
        filename = os.path.join(input_dirname, '{}.csv'.format(key))
        partial_vec_list = list(CSVLoader.load(filename))
        partial_vec_list = Sampler.sampling(partial_vec_list, SAMPLE_RATE)
        vec_list.extend(partial_vec_list)

    dim = len(vec_list[0])
    scaler.fit(vec_list)

    for mode, lang in FileManager.mode_lang:
        video_list = list()
        max_video_len = -1
        for key in FileManager.get_keys(mode, lang):
            filename_feat = os.path.join(input_dirname, '{}.csv'.format(key))

            vec_list = list(CSVLoader.load(filename_feat))
            vec_list = Sampler.sampling(vec_list, SAMPLE_RATE)
            vec_list = scaler.transform(vec_list).tolist()  # dim: (MOVIE_LENGTH,FEATURE_DIM)

            if mode == 'Test':
                label_list = [[DEFAULT_VALUE] * 3] * len(vec_list)
            else:
                filename_label = os.path.join(dir_labels, '{}.csv'.format(key))
                label_list = list(CSVLoader.load(filename_label))[:-1]

            if len(vec_list) - 1 == len(label_list):
                vec_list = vec_list[:-1]

            if len(label_list) != len(vec_list):
                raise Exception('fail {}'.format(key))

            if len(vec_list) > max_video_len:
                max_video_len = len(vec_list)

            video = list(zip(vec_list, label_list))
            video_list.append(video)

        n_batch = int(math.ceil(max_video_len / batch_size))

        vec_batch_list, label_batch_list, seq_batch_list = list(), list(), list()
        for i in range(n_batch):
            vec_batch, label_batch, seq_batch = list(), list(), list()
            for video in video_list:
                partial_vec_list, partial_label_list, seq_len = get_batch_from_video(video, batch_size, i, dim)
                vec_batch.append(partial_vec_list)
                label_batch.append(partial_label_list)
                seq_batch.append(seq_len)
            vec_batch_list.append(vec_batch)
            label_batch_list.append(label_batch)
            seq_batch_list.append(seq_batch)

        dirname = os.path.join(dir_output, input_dirname + '-1')
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        output_filename = os.path.join(dirname, '{}_{}.npz'.format(mode, lang))
        np.savez(output_filename, x=vec_batch_list, y=label_batch_list, seq_len=seq_batch_list)


if __name__ == '__main__':
    commandr.Run()
