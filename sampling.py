# -*- coding: utf-8 -*-
import numpy as np


class Sampler(object):
    @classmethod
    def sampling(cls, vec_list, n):
        new_vec_list = list()
        start_idx = 0
        while start_idx < len(vec_list):
            end_idx = start_idx + n
            partial_list = vec_list[start_idx: end_idx]
            new_vec = np.asarray(partial_list).mean(axis=0)
            new_vec_list.append(new_vec)

            start_idx = end_idx
        return new_vec_list
