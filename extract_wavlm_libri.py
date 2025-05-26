#!/usr/bin/env python

"""
Extract WavLM features for a LibriSpeech set.

Author: Herman Kamper
Date: 2024
"""

from pathlib import Path
from tqdm import tqdm
import argparse
import numpy as np
import sys
import torch
import torchaudio

from utils import pca_transform

device = "cuda"


def check_argv():
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    parser.add_argument(
        "librispeech_dir",
        type=Path,
        help="LibriSpeech directory ending in e.g. `dev-clean/`",
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        help="output will be written to a `wavlm/` subdirectory",
    )
    parser.add_argument(
        "--pca",
        type=Path,
        help="NumPy archive with PCA parameters (default: no PCA)",
    )
    parser.add_argument(
        "--exclude",
        type=Path,
        help="exclude utterances with filenames in this file",
    )
    return parser.parse_args()


def main(args):
    wavlm = torch.hub.load(
        "bshall/knn-vc", "wavlm_large", trust_repo=True, device=device
    )

    if args.pca is not None:
        print("Reading:", args.pca)
        pca = np.load(args.pca)
        temp = {}
        for key in pca:
            temp[key] = torch.from_numpy(pca[key]).float().to(device)
        pca = temp
    else:
        pca = None

    if args.exclude is not None:
        print("Reading:", args.exclude)
        exclude_utterances = set()
        with open(args.exclude) as f:
            for line in f:
                exclude_utterances.add(line.strip())

    wav_dir = args.librispeech_dir
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    print("Writing to:", output_dir)
    for speaker_dir in tqdm(sorted(wav_dir.glob("*"))):
        speaker = speaker_dir.stem
        output_fn = (output_dir / speaker).with_suffix(".npy")
        # if output_fn.is_file():
        #     continue

        features = []
        for wav_fn in tqdm(sorted(speaker_dir.rglob("*/*.flac")), leave=False):
            if wav_fn.stem in exclude_utterances:
                continue
            wav, _ = torchaudio.load(wav_fn)
            wav = wav.to(device)
            with torch.inference_mode():
                x, _ = wavlm.extract_features(wav, output_layer=6)
            if pca is not None:
                x = pca_transform(
                    x, pca["mean"], pca["components"], pca["explained_variance"]
                )
            x = x.cpu().numpy().squeeze()
            features.append(x)

        features = np.vstack(features, dtype=np.float16)
        np.save(output_fn, features)


if __name__ == "__main__":
    args = check_argv()
    main(args)
