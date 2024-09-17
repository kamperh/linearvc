#!/usr/bin/env python

"""
Perform ASR and evaluate WER in order to measure intelligibility.

Author: Herman Kamper
Date: 2024
"""

from pathlib import Path
from tqdm import tqdm
import argparse
import jiwer
import numpy as np
import random
import whisper


def check_argv():
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
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
        "--whisper",
        default="small",
        type=str,
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper size (default: small)",
    )
    parser.add_argument(
        "--format", choices=["librispeech", "vctk"], default="vctk"
    )
    return parser.parse_args()


def main(args):
    # Transcriptions
    print("Reading:", args.groundtruth_dir)
    transcript = {}
    if args.format == "librispeech":
        for transcript_fn in tqdm(
            sorted(args.groundtruth_dir.rglob("*.trans.txt"))
        ):
            with open(transcript_fn) as f:
                for line in f:
                    line = line.strip().split()
                    transcript[line[0]] = " ".join(line[1:])
    elif args.format == "vctk":
        for transcript_fn in tqdm(sorted(args.groundtruth_dir.rglob("*.txt"))):
            with open(transcript_fn) as f:
                for line in f:
                    line = line.strip()
                transcript[transcript_fn.stem] = line

    # ASR
    model = whisper.load_model(args.whisper, device="cuda")

    print("Reading:", args.converted_dir)
    labels = []
    predictions = []
    for wav_fn in tqdm(sorted(args.converted_dir.rglob("*.wav"))):
        transcript_hat = model.transcribe(str(wav_fn), language="english")
        predictions.append(transcript_hat["text"])

        if args.format == "librispeech":
            transcript_key = wav_fn.parent.stem
        elif args.format == "vctk":
            transcript_key = wav_fn.stem
        labels.append(transcript[transcript_key])

    # eval_transform = jiwer.Compose(
    #     [
    #         jiwer.ToLowerCase(),
    #         jiwer.RemoveWhiteSpace(replace_by_space=True),
    #         jiwer.RemoveMultipleSpaces(),
    #         jiwer.RemovePunctuation(),
    #         jiwer.transforms.ReduceToListOfListOfWords(),
    #     ]
    # )
    # wer = jiwer.wer(
    #     labels,
    #     predictions,
    #     hypothesis_transform=eval_transform_wer,
    #     truth_transform=eval_transform_wer,
    # )
    # print(f"WER: {wer*100:.2f}%")

    # WER: Bootstrap confidence interval
    eval_transform_wer = jiwer.Compose(
        [
            jiwer.ToLowerCase(),
            jiwer.RemoveWhiteSpace(replace_by_space=True),
            jiwer.RemoveMultipleSpaces(),
            jiwer.RemovePunctuation(),
            jiwer.transforms.ReduceToListOfListOfWords(),
        ]
    )
    random.seed(13)
    wers = []
    n_repeat = 100
    indices = list(range(len(labels)))
    print("WER bootstrap sampling:")
    for i in tqdm(range(n_repeat)):
        sample_indices = random.choices(indices, k=len(indices))
        sample_labels = [labels[i] for i in sample_indices]
        sample_predictions = [predictions[i] for i in sample_indices]
        sample_wer = jiwer.wer(
            sample_labels,
            sample_predictions,
            hypothesis_transform=eval_transform_wer,
            truth_transform=eval_transform_wer,
        )
        wers.append(sample_wer)
    wer_mean = np.mean(wers) * 100
    wer_std = np.std(wers) * 100
    print(f"WER: {wer_mean:.2f}% +- {wer_std:.2f}%")

    # CER: Bootstrap confidence interval
    eval_transform_cer = jiwer.Compose(
        [
            jiwer.ToLowerCase(),
            jiwer.RemoveWhiteSpace(replace_by_space=True),
            jiwer.RemoveMultipleSpaces(),
            jiwer.RemovePunctuation(),
            jiwer.transforms.ReduceToListOfListOfChars(),
        ]
    )
    random.seed(13)
    cers = []
    n_repeat = 100
    indices = list(range(len(labels)))
    print("CER bootstrap sampling:")
    for i in tqdm(range(n_repeat)):
        sample_indices = random.choices(indices, k=len(indices))
        sample_labels = [labels[i] for i in sample_indices]
        sample_predictions = [predictions[i] for i in sample_indices]
        sample_cer = jiwer.cer(
            sample_labels,
            sample_predictions,
            hypothesis_transform=eval_transform_cer,
            truth_transform=eval_transform_cer,
        )
        cers.append(sample_cer)
    cer_mean = np.mean(cers) * 100
    cer_std = np.std(cers) * 100
    print(f"CER: {cer_mean:.2f}% +- {cer_std:.2f}%")


if __name__ == "__main__":
    args = check_argv()
    main(args)
