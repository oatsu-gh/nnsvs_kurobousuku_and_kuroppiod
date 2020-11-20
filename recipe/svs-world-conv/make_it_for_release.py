#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) oatsu
"""
配布用フォルダを準備する
"""

from glob import glob
from os import makedirs
from shutil import copy2, copytree

from tqdm import tqdm

SINGER = 'kuroppoid'
CONFIG_DIR = 'conf'
DICTIONARY_DIR = 'dic'
RELEASE_DIR = 'release/kuroppoid_---'
PATH_QUESTION = 'hed/jp_qst_crazy_mono_005_173D.hed'
NAME_EXPERIMENT = 'jp_qst_crazy_mono_005_173D'


def copy_train_config(config_dir, release_dir):
    """
    acoustic_*.yaml, duration_*.yaml, timelag_*.yaml をコピー
    """
    print('copying config')
    copytree(config_dir, f'{release_dir}/{config_dir}')


def copy_dictionary(dictionary_dir, release_dir):
    """
    *.table, *.conf をコピー
    """
    print('copying dictionary')
    copytree(dictionary_dir, f'{release_dir}/{dictionary_dir}')


def copy_question(path_question, release_dir):
    """
    hedファイル(question)をコピー
    """
    makedirs(f'{release_dir}/hed', exist_ok=True)
    print('copying question')
    copy2(path_question, f'{release_dir}/{path_question}')


def copy_scaler(singer, release_dir):
    """
    dumpフォルダにあるファイルをコピー
    """
    makedirs(f'{release_dir}/dump/{singer}/norm', exist_ok=True)
    list_path_scaler = glob(f'dump/{singer}/norm/*_scaler.joblib')

    print('copying scaler')
    for path_scaler in tqdm(list_path_scaler):
        copy2(path_scaler, f'{release_dir}/{path_scaler}')


def copy_model(singer, name_exp, release_dir):
    """
    name_exp: 試験のID
    """
    name_exp = singer + '_' + name_exp
    makedirs(f'{release_dir}/exp/{name_exp}/acoustic', exist_ok=True)
    makedirs(f'{release_dir}/exp/{name_exp}/duration', exist_ok=True)
    makedirs(f'{release_dir}/exp/{name_exp}/timelag', exist_ok=True)
    list_path_model = glob(f'exp/{name_exp}/*/best_loss.pth')
    list_path_model += glob(f'exp/{name_exp}/*/latest.pth')
    list_path_model += glob(f'exp/{name_exp}/*/model.yaml')

    print('copying model')
    for path_model in tqdm(list_path_model):
        copy2(path_model, f'{release_dir}/{path_model}')


def main():
    """
    各種ファイルをコピーする
    """
    copy_train_config(CONFIG_DIR, RELEASE_DIR)
    copy_dictionary(DICTIONARY_DIR, RELEASE_DIR)
    copy_question(PATH_QUESTION, RELEASE_DIR)
    copy_scaler(SINGER, RELEASE_DIR)
    copy_model(SINGER, NAME_EXPERIMENT, RELEASE_DIR)


if __name__ == '__main__':
    main()
