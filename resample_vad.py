#!/usr/bin/env python

"""
Resample and perform VAD on a dataset.

Author: Herman Kamper
Date: 2024
"""

from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from tqdm import tqdm
import argparse
import itertools
import numpy as np
import torchaudio
import torchaudio.functional as F

# English speakers
speakers = [
    "p225",
    "p226",
    "p227",
    "p228",
    "p229",
    "p230",
    "p231",
    "p232",
    "p233",
    "p239",
    "p240",
    "p243",
    "p244",
    "p250",
    "p254",
    "p256",
    "p257",
    "p258",
    "p259",
    "p267",
    "p269",
    "p270",
    "p273",
    "p274",
    "p276",
    "p277",
    "p278",
    "p279",
    "p282",
    "p286",
    "p287",
]


def check_argv():
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    parser.add_argument("speaker_fn", type=Path)
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument(
        "--sample_rate", type=int, default=16000, help="default: 16000"
    )
    return parser.parse_args()


def resample_vad_wav(input_fn, output_fn, target_sr):
    # Resample
    wav, sr = torchaudio.load(input_fn)
    wav = F.resample(wav, sr, target_sr)

    # Trim silence at beginning
    wav = F.vad(wav, target_sr)
    if wav.shape[-1] == 0:
        print("Warning: Skipping:", input_fn)
        return 0

    # # Trim silence at end
    # wav, _ = torchaudio.sox_effects.apply_effects_tensor(
    #     wav, target_sr, [["reverse"]]
    # )
    # wav = F.vad(wav, target_sr)
    # if wav.shape[-1] == 0:
    #     # print("Warning: Skipping", input_fn)
    #     return 0
    # wav, sr = torchaudio.sox_effects.apply_effects_tensor(
    #     wav, target_sr, [["reverse"]]
    # )

    torchaudio.save(output_fn, wav, target_sr)
    return wav.shape[-1] / target_sr


def main(args):
    print("Reading from:", args.input_dir)
    input_wav_fns = list(args.input_dir.rglob("*.wav"))

    print("Reading:", args.speaker_fn)
    with open(args.speaker_fn) as f:
        speakers = [line.strip() for line in f.readlines()]

    input_wav_fns = [i for i in input_wav_fns if i.parent.stem in speakers]

    output_wav_fns = []
    for input_wav_fn in input_wav_fns:
        output_wav_fn = args.output_dir / input_wav_fn.relative_to(
            args.input_dir
        )
        output_wav_fn.parent.mkdir(parents=True, exist_ok=True)
        output_wav_fns.append(output_wav_fn)

    print("Writing to:", args.output_dir)
    with ProcessPoolExecutor(max_workers=4) as executor:
        results = list(
            tqdm(
                executor.map(
                    resample_vad_wav,
                    input_wav_fns,
                    output_wav_fns,
                    itertools.repeat(args.sample_rate),
                ),
                total=len(input_wav_fns),
            )
        )
    print(f"Duration: {np.sum(results) / 60 / 60:.2f} hours")


if __name__ == "__main__":
    args = check_argv()
    main(args)
