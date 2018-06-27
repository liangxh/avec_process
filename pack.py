# -*- coding: utf-8 -*-
import os
import commandr
from file_manager import FileManager
from csv_loader import CSVLoader
import math
from sklearn import preprocessing
from sampling import Sampler
import numpy as np
from sklearn.decomposition import PCA


DEFAULT_VALUE = -9999.

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
def pack(input_dir, batch_size, sample_rate, pca_dim=0):
    pca_dim = int(pca_dim)
    batch_size = int(batch_size)
    sample_rate = int(sample_rate)
    input_dirname = os.path.join(dir_root, input_dir)

    vec_list = list()
    for key in FileManager.get_keys('train'):
        filename = os.path.join(input_dirname, '{}.csv'.format(key))
        partial_vec_list = list(CSVLoader.load(filename))
        if sample_rate > 1:
            partial_vec_list = Sampler.sampling(partial_vec_list, sample_rate)
        vec_list.extend(partial_vec_list)

    dim = len(vec_list[0])
    pca = None
    if pca_dim > 0:
        pca = PCA(n_components=pca_dim)
        vec_list = pca.fit_transform(vec_list)

    scaler = preprocessing.StandardScaler()
    scaler.fit(vec_list)

    for mode, lang in FileManager.mode_lang:
        video_list = list()
        max_video_len = -1
        for key in FileManager.get_keys(mode, lang):
            filename_feat = os.path.join(input_dirname, '{}.csv'.format(key))

            vec_list = list(CSVLoader.load(filename_feat))
            if sample_rate > 1:
                vec_list = Sampler.sampling(vec_list, sample_rate)

            if pca_dim > 0:
                vec_list = pca.transform(vec_list)

            vec_list = scaler.transform(vec_list).tolist()  # dim: (MOVIE_LENGTH,FEATURE_DIM)

            if mode == 'Test':
                label_list = [[DEFAULT_VALUE] * 3] * len(vec_list)
            else:
                filename_label = os.path.join(dir_labels, '{}.csv'.format(key))
                label_list = list(CSVLoader.load(filename_label))

            if len(vec_list) + 1 == len(label_list):
                vec_list = [[0.] * dim] + vec_list
            elif len(vec_list) - 1 == len(label_list):
                vec_list = vec_list[1:]
            elif len(label_list) != len(vec_list):
                raise Exception('fail {}: {} != {}'.format(key, len(label_list), len(vec_list)))

            if len(vec_list) > max_video_len:
                max_video_len = len(vec_list)

            video_list.append((vec_list, label_list))

        # GROUP-1

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

        dirname = os.path.join(dir_output, input_dir + '-1')
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        output_filename = os.path.join(dirname, '{}_{}.npz'.format(mode, lang))
        np.savez(output_filename, x=vec_batch_list, y=label_batch_list, seq_len=seq_batch_list)

        # GROUP-2

        vec_list, label_list, seq_list = list(), list(), list()
        for video in video_list:
            _vec_list, _label_list = video
            video_len = len(_vec_list)
            n_clip = int(math.ceil(video_len / batch_size))
            for i in range(n_clip):
                partial_vec_list, partial_label_list, seq_len = get_batch_from_video(video, batch_size, i, dim)
                vec_list.append(partial_vec_list)
                label_list.append(partial_label_list)
                seq_list.append(seq_len)

        dirname = os.path.join(dir_output, input_dir + '-2')
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        output_filename = os.path.join(dirname, '{}_{}.npz'.format(mode, lang))
        np.savez(output_filename, x=vec_list, y=label_list, seq_len=seq_list)


if __name__ == '__main__':
    commandr.Run()
