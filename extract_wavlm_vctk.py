#!/usr/bin/env python

"""
Extract WavLM features for VCTK parallel utterances.

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

device = "cuda"


def check_argv():
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    parser.add_argument("wav_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument(
        "--utterance",
        type=str,
        help="only extract features for this utterance"
        " (default: all utterances)",
    )
    return parser.parse_args()


def main(args):
    wavlm = torch.hub.load(
        "bshall/knn-vc", "wavlm_large", trust_repo=True, device=device
    )

    args.output_dir.mkdir(parents=True, exist_ok=True)

    print("Writing to:", args.output_dir)
    for speaker_dir in tqdm(sorted(args.wav_dir.glob("*"))):
        speaker = speaker_dir.stem
        output_fn = (args.output_dir / speaker).with_suffix(".npy")

        if args.utterance is not None:
            wav_fn = speaker_dir / f"{speaker}_{args.utterance}.wav"
            if not wav_fn.is_file():
                print("Warning: Missing:", wav_fn)
                continue

            wav, _ = torchaudio.load(wav_fn)
            wav = wav.to(device)
            with torch.inference_mode():
                feats, _ = wavlm.extract_features(wav, output_layer=6)
            feats = feats.cpu().numpy().squeeze()
            feats = np.float16(feats)
            np.save(output_fn, feats)

        else:
            features = []
            for wav_fn in tqdm(sorted(speaker_dir.rglob("*.wav")), leave=False):
                wav, _ = torchaudio.load(wav_fn)
                wav = wav.to(device)
                with torch.inference_mode():
                    x, _ = wavlm.extract_features(wav, output_layer=6)
                x = x.cpu().numpy().squeeze()
                features.append(x)

            features = np.vstack(features, dtype=np.float16)
            np.save(output_fn, features)


if __name__ == "__main__":
    args = check_argv()
    main(args)
