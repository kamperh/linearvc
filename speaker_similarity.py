#!/usr/bin/env python

"""
Evaluate speaker similarity using EER (lower corresponds to better conversion).

Author: Benjamin van Niekerk, Herman Kamper
Date: 2023, 2024
"""

from pathlib import Path
from scipy.interpolate import interp1d
from scipy.optimize import brentq
from scipy.spatial.distance import cosine
from sklearn.metrics import roc_curve
from speechbrain.inference.speaker import EncoderClassifier
from tqdm import tqdm
import argparse
import numpy as np
import pandas
import sys
import torch
import torchaudio
import torchaudio.functional as F

device = "cuda"


def check_argv():
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    parser.add_argument(
        "eval_csv", type=str, help="evaluation CSV listing utterance pairs"
    )
    parser.add_argument(
        "converted_dir",
        type=Path,
        help="converted speech directory",
    )
    parser.add_argument(
        "groundtruth_dir",
        type=Path,
        help="real speech directory; for LibriSpeech, this would end in "
        "e.g. `dev-clean`",
    )
    parser.add_argument(
        "--format", choices=["librispeech", "vctk"], default="vctk"
    )
    parser.add_argument(
        "--zero_positive",
        help="in some cases you want the 0 label in the evaluation CSV "
        "to indicate a positive sample (instead of the usual 1 label)",
        action="store_true",
    )
    return parser.parse_args()


def eer(y, y_score):
    fpr, tpr, _ = roc_curve(y, 1 - y_score, pos_label=1)
    return brentq(lambda x: 1.0 - x - interp1d(fpr, tpr)(x), 0.0, 1.0)


def speaker_similarity(args):
    classifier = EncoderClassifier.from_hparams(
        source="speechbrain/spkrec-xvect-voxceleb",
        savedir="pretrained_models/spkrec-xvect-voxceleb",
        run_opts={"device": "cuda"},
    )

    pairs = pandas.read_csv(args.eval_csv)

    # print(pairs)

    converted_pairs = pairs[pairs.label == 0]
    groundtruth_paris = pairs[pairs.label == 1]

    # print(pairs)
    # assert False

    scores = []

    # Converted similarities
    for _, (
        source_speaker,
        target_speaker,
        source_key,
        target_key,
        label,
    ) in tqdm(list(converted_pairs.iterrows())):
        source_wav_fn = (args.converted_dir / source_key).with_suffix(".wav")
        if args.format == "librispeech":
            target_wav_fn = (args.groundtruth_dir / target_key).with_suffix(
                ".flac"
            )
        elif args.format == "vctk":
            target_wav_fn = (args.groundtruth_dir / target_key).with_suffix(
                ".wav"
            )

        x, sr = torchaudio.load(source_wav_fn)
        y, sr = torchaudio.load(target_wav_fn)
        x = F.resample(x, sr, 16000)
        y = F.resample(y, sr, 16000)
        x = x.to(device)
        y = y.to(device)

        x = classifier.encode_batch(x).squeeze().cpu().numpy()
        y = classifier.encode_batch(y).squeeze().cpu().numpy()

        if args.zero_positive:
            label = 1

        scores.append((source_speaker, target_speaker, cosine(x, y), label))

    # Ground truth similarities
    for _, (
        source_speaker,
        target_speaker,
        source_key,
        target_key,
        label,
    ) in tqdm(list(groundtruth_paris.iterrows())):
        if args.format == "librispeech":
            source_wav_fn = (args.groundtruth_dir / source_key).with_suffix(
                ".flac"
            )
            target_wav_fn = (args.groundtruth_dir / target_key).with_suffix(
                ".flac"
            )
        elif args.format == "vctk":
            source_wav_fn = (args.groundtruth_dir / source_key).with_suffix(
                ".wav"
            )
            target_wav_fn = (args.groundtruth_dir / target_key).with_suffix(
                ".wav"
            )

        x, sr = torchaudio.load(source_wav_fn)
        y, sr = torchaudio.load(target_wav_fn)
        x = F.resample(x, sr, 16000)
        y = F.resample(y, sr, 16000)
        x = x.to(device)
        y = y.to(device)

        x = classifier.encode_batch(x).squeeze().cpu().numpy()
        y = classifier.encode_batch(y).squeeze().cpu().numpy()

        if args.zero_positive:
            label = 0

        scores.append((source_speaker, target_speaker, cosine(x, y), label))

    scores = pandas.DataFrame(
        scores, columns=["src_speaker", "tgt_speaker", "score", "label"]
    )

    sim = (
        scores.groupby("tgt_speaker")
        .apply(lambda x: eer(x.label, x.score))
        .reset_index(name="eer")
    )
    print(sim.agg(mean=("eer", np.mean), std=("eer", np.std)))


if __name__ == "__main__":
    args = check_argv()
    speaker_similarity(args)
