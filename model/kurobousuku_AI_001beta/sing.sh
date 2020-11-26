#!/bin/bash
# Copyright (c) 2020 Ryuichi Yamamoto
# Copyright (c) 2020 Tarou Shirani
# Copyright (c) 2020 oatsu

# wsl run.sh で実行するとPATHが皆無なので登録する
PATH="$HOME/.local/bin:$PATH"

script_dir=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
. $script_dir/utils/yaml_parser.sh || exit 1;

# 設定を展開し、変数として記憶する
eval $(parse_yaml "./config.yaml" "")

dump_norm_dir=dump/$spk/norm

. $nnsvs_root/utils/yaml_parser.sh || exit 1;

# exp name / 音声モデルを判別するための名前
if [ -z ${tag:=} ]; then
    expname=${spk}
else
    expname=${spk}_${tag}
fi
expdir=exp/$expname

# 音声出力フォルダを作成
mkdir -p $out_wav_dir

# 音声ファイルを生成
nnsvs-synthesis \
    question_path=$question_path \
    timelag=$timelag_synthesis \
    duration=$duration_synthesis \
    acoustic=$acoustic_synthesis \
    timelag.checkpoint=$expdir/timelag/$timelag_eval_checkpoint \
    timelag.in_scaler_path=$dump_norm_dir/in_timelag_scaler.joblib \
    timelag.out_scaler_path=$dump_norm_dir/out_timelag_scaler.joblib \
    timelag.model_yaml=$expdir/timelag/model.yaml \
    duration.checkpoint=$expdir/duration/best_loss.pth \
    duration.in_scaler_path=$dump_norm_dir/in_duration_scaler.joblib \
    duration.out_scaler_path=$dump_norm_dir/out_duration_scaler.joblib \
    duration.model_yaml=$expdir/duration/model.yaml \
    acoustic.checkpoint=$expdir/acoustic/latest.pth \
    acoustic.in_scaler_path=$dump_norm_dir/in_acoustic_scaler.joblib \
    acoustic.out_scaler_path=$dump_norm_dir/out_acoustic_scaler.joblib \
    acoustic.model_yaml=$expdir/acoustic/model.yaml \
    in_dir=$in_lab_dir \
    utt_list=$utt_list \
    out_dir=$out_wav_dir \
    ground_truth_duration=false \
    sample_rate=$sample_rate
