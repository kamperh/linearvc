#!/usr/bin/env python

"""
Create the evaluation CSV for VTCK.

Author: Herman Kamper
Date: 2024
"""

from pathlib import Path
from tqdm import tqdm
import argparse
import random

# args.wav_dir = Path("/home/kamperh/scratch/vctk/wav/")
n_utt_per_pair = 5


def check_argv():
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    parser.add_argument("speaker_fn", type=Path)
    parser.add_argument("wav_dir", type=Path)
    parser.add_argument(
        "output_csv",
        type=str,
        help="CSV of evaluation utterance pairs",
    )
    return parser.parse_args()


def main(args):
    print("Reading:", args.speaker_fn)
    with open(args.speaker_fn) as f:
        speakers = [line.strip() for line in f.readlines()]

    random.seed(13)
    print("Writing:", args.output_csv)
    n_pairs_total = 0
    with open(args.output_csv, "w") as f:
        f.write("source,target,output_fn,reference_fn,label\n")
        for source in tqdm(sorted(speakers)):
            for target in sorted(speakers):
                if target == source:
                    continue

                # Conversions
                n_pairs = 0
                i_utt = 50
                while n_pairs < n_utt_per_pair:
                    source_fn = Path(f"{source}/{source}_{i_utt:03d}.wav")
                    target_fn = Path(f"{target}/{target}_{i_utt:03d}.wav")
                    if not (
                        (args.wav_dir / source_fn).is_file()
                        and (args.wav_dir / target_fn).is_file()
                    ):
                        i_utt += 1
                        continue

                    f.write(
                        f"{source},{target}"
                        f",{source}-{target}/{source}_{i_utt:03d}.wav"
                        f",{target}/{target}_{i_utt:03d}.wav,0\n"
                    )
                    n_pairs_total += 1

                    i_utt += 1
                    n_pairs += 1

                # Ground truth
                n_pairs = 0
                i_utt = 50
                while n_pairs < n_utt_per_pair:
                    source_fn = Path(f"{source}/{source}_{i_utt:03d}.wav")

                    choices = [
                        i.stem
                        for i in sorted((args.wav_dir / f"{source}").glob("*.wav"))
                    ]
                    choices = choices[25:]  # first 24 is parallel

                    choice = random.choice(choices)
                    target_fn = Path(f"{source}/{choice}.wav")
                    while target_fn == source_fn:
                        # print("jap", source_fn, target_fn)
                        choice = random.choice(choices)
                        target_fn = Path(f"{source}/{choice}.wav")
                        # print("jap2", source_fn, target_fn)

                    # target_fn = Path(f"{target}/{target}_{i_utt:03d}.wav")
                    if not (
                        (args.wav_dir / source_fn).is_file()
                        and (args.wav_dir / target_fn).is_file()
                    ):
                        i_utt += 1
                        continue

                    f.write(f"{source},{source},{source_fn},{target_fn},1\n")
                    n_pairs_total += 1

                    i_utt += 1
                    n_pairs += 1

    print("Total no. test pairs:", n_pairs_total)


if __name__ == "__main__":
    args = check_argv()
    main(args)
