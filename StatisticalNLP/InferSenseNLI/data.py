# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import os
import numpy as np
import torch
import pandas as pd
from nltk import word_tokenize


def get_batch(batch, word_vec, emb_dim=300):
    # sent in batch in decreasing order of lengths (bsize, max_len, word_dim)
    lengths = np.array([len(x) for x in batch])
    max_len = np.max(lengths)
    embed = np.zeros((max_len, len(batch), emb_dim))

    for i in range(len(batch)):
        for j in range(len(batch[i])):
            embed[j, i, :] = word_vec[batch[i][j]]

    return torch.from_numpy(embed).float(), lengths


def get_word_dict(sentences):
    # create vocab of words
    word_dict = {}
    for sent in sentences:
        for word in sent:
            if word not in word_dict:
                word_dict[word] = ''
    word_dict['<s>'] = ''
    word_dict['</s>'] = ''
    # word_dict['<p>'] = ''
    return word_dict


def get_glove(word_dict, glove_path):
    # create word_vec with glove vectors
    word_vec = {}
    with open(glove_path, encoding="utf8") as f: # add  encoding="utf8" AGP
    
        for line in f:
            word, vec = line.split(' ', 1)
            if word in word_dict:
                word_vec[word] = np.array(list(map(float, vec.split())))
    print('Found {0}(/{1}) words with glove vectors'.format(
                len(word_vec), len(word_dict)))

    # for word in word_dict:
    #     if word not in word_vec:
    #         print(f'not found {word}')

    word_vec['<s>'] = np.array([0.44213, -0.13069, 0.13177, -0.020734, 0.18385, -0.24139, 0.42682, 0.6635, -0.4228, -1.3182, 0.8969, 0.069487, 0.18833, 0.64092, 0.75374, 0.47922, 0.15555, -1.3322, -0.44204, 0.35286, -0.49904, 0.22915, 0.33414, -0.056617, -0.42288, 0.30555, -0.43267, 0.21671, -0.17978, 0.0029344, -0.061375, -0.23775, 0.34494, 0.13399, -0.16143, -0.14828, 0.83514, -0.04745, -0.27438, 0.94555, -0.032422, 0.36721, -0.034479, -0.26252, -0.32278, -0.49477, 0.016184, -0.3408, -0.13057, 0.26092, 0.31645, 0.14784, 0.88557, 0.17651, 0.64041, -1.2515, 0.15421, 0.17217, -0.03236, -0.1245, -0.031818, -0.86255, 0.54778, -0.43682, -0.58938, 0.31747, -0.082669, -0.00056269, -0.31571, 0.073996, -0.11877, 0.41537, -0.2407, -0.18274, -0.015273, 0.73703, -0.27489, 0.52789, -0.15805, -0.82665, -0.082009, 0.16873, -0.22525, 0.9077, -0.29906, 0.19191, 1.0629, -0.33424, -0.77023, 0.21618, 0.39841, -0.39372, -0.17785, -0.4733, 0.26626, 0.90588, 0.25426, -0.70709, -0.20417, 0.12558, 0.41313, 0.66347, 0.24456, -0.26122, -0.24734, -0.5588, 0.33128, -0.51162, -1.1203, -0.23859, -0.35756, -0.25638, 0.24918, -0.16726, -0.22751, 0.64171, -0.63334, -0.023124, -0.028377, 0.46149, -0.4893, -0.56075, 0.54746, -0.10401, -0.034816, 0.20352, -0.68081, 0.24934, 0.2085, 0.26233, -1.1829, -0.15722, -0.25678, -0.18094, 0.78932, 0.39527, 0.57457, -0.3188, 0.27194, -1.3732, 0.43167, -0.0015873, -0.49582, -0.59358, 0.32786, 0.38705, -0.66454, 0.33186, -0.72327, -0.062305, 0.64581, 0.52623, -0.045381, 0.54648, 0.535, 0.13124, -0.12706, -0.34515, 0.18425, -0.54762, 0.51173, 0.56886, -0.45544, 0.35809, 0.21395, 0.13886, -0.35205, -0.27206, -0.0093094, 0.85505, -0.097688, 0.19081, 0.13343, 0.022211, 1.1584, -0.0054317, 0.19605, -0.40668, -0.34654, -0.51239, 0.29111, -0.3656, 0.95526, -0.13995, 0.17064, 0.45337, -0.15994, -0.11444, 0.56727, -0.23886, 0.23497, -0.51387, -0.044393, -0.052147, 0.3725, -0.41952, 0.73253, 0.24362, -0.22638, -0.36713, -0.35638, 0.22844, -0.57123, 0.37884, -0.22018, 0.12967, -0.044183, -0.77763, -0.39544, 1.0093, 0.027183, 0.14097, 0.26727, 0.080537, -0.37513, -0.37411, -0.013149, 0.37047, 0.30365, 0.35785, 0.46538, 0.67842, 0.33637, 0.018009, -0.62155, 0.27026, -0.48156, 0.01557, -0.91347, -0.59238, 0.9439, 0.20588, -0.089695, -0.47082, -0.2149, 0.15757, -0.099286, 0.31629, -0.44816, 0.090469, 0.51286, -0.18176, 0.21942, -0.35102, -0.25428, -0.43933, -0.1987, -0.084199, 0.55013, 0.19424, 0.28146, -0.10199, 0.084996, -0.012601, -0.018345, 0.48325, 0.32592, 0.35927, 0.34562, -0.30411, -0.40811, -0.43271, -0.37122, -0.74919, -0.15797, 0.56231, 0.65503, -0.65504, 0.33262, 0.18454, -0.4704, -0.67624, 0.074776, -0.19618, -0.1064, 0.052947, 0.20473, 0.034212, 0.5807, -0.48147, -0.52761, -0.30542, -0.37957, 0.30567, 0.92345, -0.1221, -0.22881, 0.26276, -0.68335, -0.29159, 0.24049, -0.19861, -0.6644, -0.254, 0.14259, 0.086271, 0.8393, -0.68668, -0.58191, -0.65844])
    word_vec['</s>'] = np.array([0.96518, -0.013793, 0.26368, -0.57558, 0.29189, -0.77419, 0.92813, 0.33491, -0.56264, -1.5055, 0.87522, 0.12121, -0.26666, 0.65117, -0.094307, 0.58815, -0.20143, -1.1183, -0.76188, 0.3703, -0.43813, 0.05144, -0.22759, 0.0026612, -0.29345, -0.060928, -0.29678, -0.39089, -0.065718, 0.027053, 0.050217, 0.30206, -0.17689, 0.56699, -0.094687, 0.27926, 0.84336, 0.27701, -0.16885, 0.54693, 0.11859, 0.75564, -0.57291, 0.21906, -0.17068, -0.55934, 0.2578, 0.048854, 0.36774, 0.032424, 0.69632, 0.19421, 0.92222, 0.52023, 0.31813, -1.2024, -0.36368, 0.42175, 0.0098592, 0.038378, -0.56618, -0.47771, -0.080746, -0.54019, -0.55936, -0.0081851, 0.34907, -0.27568, -0.16642, -0.28105, 0.04071, 0.006245, 0.31914, 0.10721, -0.088067, 0.55735, -0.75064, 0.68986, 0.64881, -0.97527, -0.12478, -0.038272, -0.88075, 0.71527, -0.39611, -0.052852, 0.6543, -0.19419, -0.76775, 0.26981, 0.68857, -0.71118, -0.070007, -0.2471, -0.27132, 0.5768, 0.10478, -1.0667, -0.70248, 0.6969, 0.67341, 0.83869, -0.037526, -0.76962, -0.69296, -0.92255, 0.76057, -0.68365, -1.5759, -0.32211, 0.034854, -0.37452, 0.40101, 0.056363, 0.23767, 0.54406, -0.5792, 0.23316, 0.20608, 0.53974, 0.1905, -0.87393, 0.58555, -0.14021, -0.32571, 0.5398, -1.0036, -0.67161, 0.077547, -0.19163, -0.81365, 0.28102, -0.1855, -0.091431, 0.52857, -0.034575, 0.26076, -0.70792, -0.23394, -0.6448, 0.017545, -0.29459, -0.63009, -0.43323, 0.46275, 0.13031, -0.6301, 0.34291, -0.087477, 0.51742, 0.13535, 0.45874, -0.35787, 0.35766, -0.33021, 0.056491, -0.3483, -0.011544, -0.27706, -0.11686, 0.75576, 0.54215, -1.0103, 0.27231, -0.19183, 0.35319, -0.25537, -0.58517, -0.058062, 0.95162, 0.13854, 0.51403, 0.2159, -0.85678, 1.3898, 0.0023125, -0.34508, -0.12618, -0.51777, -0.26025, -0.044106, 0.16772, 1.2664, -0.065463, 0.2015, 0.40627, -0.49783, -0.66239, 0.36734, -0.19947, -0.13682, -0.44856, 0.23931, 0.11568, 0.54196, -0.59561, 0.43361, 0.065241, -0.48621, -0.31566, 0.016218, 0.10498, -0.61184, 0.63551, -0.14638, 0.70817, -0.45867, -0.65949, 0.494, 0.41355, 0.30997, 0.17349, 0.47035, 0.95388, 0.021404, -0.6957, 0.25382, 0.69105, 0.78775, 0.0099848, 0.26103, 0.56733, 0.32872, -0.091424, -0.70057, 0.1178, -1.1703, 0.3448, -0.2034, -0.56501, 0.96737, 0.22182, 0.19053, 0.14226, 0.73301, -0.53171, -0.066444, 1.0141, 0.0522, 0.33255, 0.17188, -0.18769, 0.20831, -0.0014853, -0.18294, -0.75189, -0.28169, 0.012121, -0.03025, 0.32892, -0.17652, 0.1503, 0.38961, -1.0464, -0.30045, 0.0016955, 0.283, 0.54507, 0.30139, -0.68222, -0.19745, -0.6639, -0.088617, -0.69707, 0.24818, -0.022122, 0.828, -0.422, 0.44309, 0.34444, -0.5484, -0.41007, 0.26391, -0.55702, -0.65137, -0.05891, 0.10197, -0.2084, 0.41109, -0.34521, -0.61239, -0.41286, -0.83716, -0.11735, 0.60925, 0.55094, -0.84516, 0.42881, 0.22677, -0.11721, 0.24849, -0.2671, -0.90172, 0.20581, 0.43598, 0.8212, 1.1729, -0.43784, -0.31668, -0.03276])

    return word_vec


def build_vocab(sentences, glove_path):
    word_dict = get_word_dict(sentences)
    word_vec = get_glove(word_dict, glove_path)
    print('Vocab size : {0}'.format(len(word_vec)))
    return word_vec


def get_nli(data_path):
    s1 = {}
    s2 = {}
    target = {}

    dico_label = {'entailment': 0,  'neutral': 1, 'contradiction': 2}

    for data_type in ['train', 'dev', 'test']:
        s1[data_type], s2[data_type], target[data_type] = {}, {}, {}
        s1[data_type]['path'] = os.path.join(data_path, 's1.' + data_type)
        s2[data_type]['path'] = os.path.join(data_path, 's2.' + data_type)
        target[data_type]['path'] = os.path.join(data_path,
                                                 'labels.' + data_type)

        s1[data_type]['sent'] = [line.rstrip() for line in
                                 open(s1[data_type]['path'], 'r')]
        s2[data_type]['sent'] = [line.rstrip() for line in
                                 open(s2[data_type]['path'], 'r')]
        target[data_type]['data'] = np.array([dico_label[line.rstrip('\n')]
                for line in open(target[data_type]['path'], 'r')])

        assert len(s1[data_type]['sent']) == len(s2[data_type]['sent']) == \
            len(target[data_type]['data'])

        print('** {0} DATA : Found {1} pairs of {2} sentences.'.format(
                data_type.upper(), len(s1[data_type]['sent']), data_type))

    train = {'s1': s1['train']['sent'], 's2': s2['train']['sent'],
             'label': target['train']['data']}
    dev = {'s1': s1['dev']['sent'], 's2': s2['dev']['sent'],
           'label': target['dev']['data']}
    test = {'s1': s1['test']['sent'], 's2': s2['test']['sent'],
            'label': target['test']['data']}
    return train, dev, test


def tokenize(s):
    s = s.lower()
    xs = word_tokenize(s)
    return xs



def get_nli_csv(data_path):
    s1 = {}
    s2 = {}
    target = {}

    dico_label = {'entailment': 0,  'neutral': 1, 'contradiction': 2}

    for data_type in ['train', 'dev', 'test']:

        aux = 'train' if data_type=='train' else 'dev_matched' if data_type=='dev' else 'dev_mismatched'
        url = f'{data_path}multinli_1.0_{aux}.txt'
        print(url)

        df = pd.read_csv(url,  delimiter = "\t",error_bad_lines=False, na_filter=False,  encoding="utf8")
        df = df.dropna()
        df = df.reset_index(drop=True)
        # Remove the missing label row
        df = df[df['gold_label'] != '-']
        #df = df[-~df['gold_label'].isin(['neutral', 'entailment', 'contradiction'])]

        s1[data_type], s2[data_type], target[data_type] = {}, {}, {}
        # s1[data_type]['path'] = os.path.join(data_path, 's1.' + data_type)
        # s2[data_type]['path'] = os.path.join(data_path, 's2.' + data_type)
        # target[data_type]['path'] = os.path.join(data_path, 'labels.' + data_type)

        s1[data_type]['sent'] = list(map(lambda x: tokenize(x), df['sentence1'].to_list()))
        s2[data_type]['sent'] = list(map(lambda x: tokenize(x), df['sentence2'].to_list()))
        target[data_type]['data'] = np.array([dico_label[v] for v in df['gold_label'].values])

        assert len(s1[data_type]['sent']) == len(s2[data_type]['sent']) == \
            len(target[data_type]['data'])

        print('** {0} DATA : Found {1} pairs of {2} sentences.'.format(
                data_type.upper(), len(s1[data_type]['sent']), data_type))

    train = {'s1': s1['train']['sent'], 's2': s2['train']['sent'], 'label': target['train']['data']}
    dev = {'s1': s1['dev']['sent'], 's2': s2['dev']['sent'], 'label': target['dev']['data']}
    test = {'s1': s1['test']['sent'], 's2': s2['test']['sent'], 'label': target['test']['data']}
    return train, dev, test


def get_nli_csv_snli(data_path):
    s1 = {}
    s2 = {}
    target = {}

    dico_label = {'entailment': 0,  'neutral': 1, 'contradiction': 2}

    for data_type in ['train', 'dev', 'test']:
        df = pd.read_csv(f'{data_path}/snli_1.0_{data_type}.csv', na_filter=False)
        df = df[df['gold_label'] != '-']

        s1[data_type], s2[data_type], target[data_type] = {}, {}, {}
        # s1[data_type]['path'] = os.path.join(data_path, 's1.' + data_type)
        # s2[data_type]['path'] = os.path.join(data_path, 's2.' + data_type)
        # target[data_type]['path'] = os.path.join(data_path, 'labels.' + data_type)

        s1[data_type]['sent'] = list(map(lambda x: tokenize(x), df['sentence1'].to_list()))
        s2[data_type]['sent'] = list(map(lambda x: tokenize(x), df['sentence2'].to_list()))
        target[data_type]['data'] = np.array([dico_label[v] for v in df['gold_label'].values])

        assert len(s1[data_type]['sent']) == len(s2[data_type]['sent']) == \
            len(target[data_type]['data'])

        print('** {0} DATA : Found {1} pairs of {2} sentences.'.format(
                data_type.upper(), len(s1[data_type]['sent']), data_type))

    train = {'s1': s1['train']['sent'], 's2': s2['train']['sent'], 'label': target['train']['data']}
    dev = {'s1': s1['dev']['sent'], 's2': s2['dev']['sent'], 'label': target['dev']['data']}
    test = {'s1': s1['test']['sent'], 's2': s2['test']['sent'], 'label': target['test']['data']}
    return train, dev, test