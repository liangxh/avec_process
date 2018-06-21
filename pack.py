# -*- coding: utf-8 -*-
import os
import commandr
from file_manager import FileManager
from csv_loader import CSVLoader
from sklearn import preprocessing
from sampling import Sampler


dir_output = '/home/lxh12/AVEC2018_data'
dir_root = '/home/lxh12/AVEC2018_CES'
dir_labels = os.path.join(dir_root, 'labels')


@commandr.command('pack')
def pack(input_dirname, output_filename):
    input_dirname = os.path.join(dir_root, input_dirname)

    '''
    scaler = preprocessing.StandardScaler()
    vec_list = list()
    for key in FileManager.get_keys('train'):
        filename = os.path.join(input_dirname, '{}.csv'.format(key))
        partial_vec_list = CSVLoader.load(filename)
        partial_vec_list = Sampler.sampling(partial_vec_list, 5)
        vec_list.extend(partial_vec_list)

    dim = len(vec_list[0])
    scaler.fit(vec_list)
    '''

    for mode, lang in FileManager.mode_lang:
        vec_list = list()  # dim: (N_MOVIES, MOVIE_LENGTH,FEATURE_DIM)
        for key in FileManager.get_keys(mode, lang):
            filename_feat = os.path.join(input_dirname, '{}.csv'.format(key))

            partial_vec_list = list(CSVLoader.load(filename_feat))
            partial_vec_list = Sampler.sampling(partial_vec_list, 5)
            #partial_vec_list = scaler.transform(partial_vec_list).tolist()
            vec_list.extend(partial_vec_list)

            if mode == 'Test':
                label_list = [[-1, -1, -1]] * len(partial_vec_list)
            else:
                filename_label = os.path.join(dir_labels, '{}.csv'.format(key))
                label_list = list(CSVLoader.load(filename_label))

            if len(label_list) != len(partial_vec_list):
                raise Exception('fail {}'.format(key))


if __name__ == '__main__':
    commandr.Run()
