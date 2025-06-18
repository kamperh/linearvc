#!/usr/bin/env python

"""
Perform voice conversion with linear regression.

Author: Herman Kamper
Date: 2024
"""

from pathlib import Path
from tqdm import tqdm
import argparse
import torch
import torch.nn as nn
import torchaudio
import torchaudio.functional as F

from utils import fast_cosine_dist

n_frames_max = 8192  # maximum no. of matched frames in linear regression
k_top = 1


class LinearVC(nn.Module):
    def __init__(self, wavlm, hifigan, device="cuda"):
        super().__init__()
        self.wavlm = wavlm.eval()
        self.hifigan = hifigan.eval()
        self.device = device
        self.sr = 16000

    @torch.inference_mode()
    def get_features(self, wav_fn, vad=False):
        """
        Return features of `wav_fn` as a tensor with shape (n_frames, dim).

        VAD is applied by default.
        """

        wav, sr = torchaudio.load(wav_fn)
        wav = wav.to(self.device)

        if not sr == self.sr:
            wav = F.resample(
                wav,
                orig_freq=sr,
                new_freq=self.sr,
                trigger_level=vad_trigger_level,
            )

        # Trim silence at beginning (if specified)
        if vad:
            wav = F.vad(wav, self.sr)

        features, _ = self.wavlm.extract_features(wav, output_layer=6)
        features = features.squeeze()

        return features

    @torch.inference_mode()
    def get_projmat(
        self, source_wavs, target_wavs, parallel=False, lasso=None, vad=False
    ):
        if parallel and lasso is None:
            lasso = 0.3

        if not parallel:
            # Source features
            source_features = []
            print("Source features:")
            for wav_fn in tqdm(sorted(source_wavs), leave=True):
                source_features.append(self.get_features(wav_fn, vad))
            source_features = torch.vstack(source_features)[:n_frames_max, :]

            # Target features
            target_features = []
            print("Target features:")
            for wav_fn in tqdm(sorted(target_wavs), leave=True):
                target_features.append(self.get_features(wav_fn, vad))
            target_features = torch.vstack(target_features)[:n_frames_max, :]

            # Matching
            dists = fast_cosine_dist(
                source_features, target_features, device=self.device
            )
            best = dists.topk(k=k_top, largest=False, dim=-1)
            linear_target = target_features[best.indices].mean(dim=1)
        else:
            # Audio with the same name: parallel utterance pairs
            source_target_wav_pairs = []
            for source_wav_fn in sorted(source_wavs):
                for target_wav_fn in sorted(target_wavs):
                    if source_wav_fn.name == target_wav_fn.name:
                        source_target_wav_pairs.append(
                            (source_wav_fn, target_wav_fn)
                        )

            # Inputs and outputs for linear regression
            combined_source_feats = []
            combined_linear_target = []
            for source_wav_fn, target_wav_fn in tqdm(source_target_wav_pairs):
                # Features
                source_features = self.get_features(source_wav_fn, vad)
                target_features = self.get_features(target_wav_fn, vad)

                # Matching
                dists = fast_cosine_dist(
                    source_features, target_features, device=self.device
                )
                best = dists.topk(k=k_top, largest=False, dim=-1)
                linear_target = target_features[best.indices].mean(dim=1)

                combined_source_feats.append(source_features)
                combined_linear_target.append(linear_target)

            source_features = torch.vstack(combined_source_feats)
            linear_target = torch.vstack(combined_linear_target)

        # Projection matrix
        if lasso is None:
            from numpy import linalg

            W, _, _, _ = linalg.lstsq(
                source_features.cpu(), linear_target.cpu(), rcond=None
            )
        else:
            import celer

            print(f"Lasso with alpha: {lasso:.2f}")

            linear = celer.Lasso(alpha=lasso, fit_intercept=False).fit(
                source_features.cpu().numpy(), linear_target.cpu().numpy()
            )
            W = linear.coef_.T

        W = torch.from_numpy(W).float().to(self.device)
        return W

    @torch.inference_mode()
    def project_and_vocode(self, input_features, W):
        """Return the waveform samples."""
        source_to_target_feats = input_features[None] @ W
        wav_hat = self.hifigan(source_to_target_feats).squeeze(0)
        return wav_hat.cpu().squeeze().cpu()


def check_argv():
    parser = argparse.ArgumentParser(description=__doc__.strip().split("\n")[0])
    parser.add_argument(
        "source_wav_dir", type=Path, help="directory with source speaker speech"
    )
    parser.add_argument(
        "target_wav_dir", type=Path, help="directory with target speaker speech"
    )
    parser.add_argument("input_wav", type=Path, help="input speech filename")
    parser.add_argument("output_wav", type=Path, help="output speech filename")
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="whether source and target utterances are parallel,"
        " in which case the filenames in the two directories should match",
    )
    parser.add_argument(
        "--lasso", type=float, help="lasso is applied with this alpha value"
    )
    parser.add_argument(
        "--vad",
        action="store_true",
        help="voice activatiy detecion is applied to start of utterance",
    )
    parser.add_argument(
        "--extension",
        choices=[".flac", ".wav"],
        help="source and target audio file extension (default: '.wav')",
        default=".wav",
    )
    return parser.parse_args()


def main(args):
    device = "cuda"

    # Load the WavLM feature extractor and HiFiGAN vocoder
    wavlm = torch.hub.load(
        "bshall/knn-vc",
        "wavlm_large",
        trust_repo=True,
        progress=True,
        device=device,
    )
    hifigan, _ = torch.hub.load(
        "bshall/knn-vc",
        "hifigan_wavlm",
        trust_repo=True,
        prematched=True,
        progress=True,
        device=device,
    )

    linearvc_model = LinearVC(wavlm, hifigan, device)

    # Lists of source and target audio files
    print("Reading from:", args.source_wav_dir)
    source_wavs = list(args.source_wav_dir.rglob("*" + args.extension))
    print("Reading from:", args.target_wav_dir)
    target_wavs = list(args.target_wav_dir.rglob("*" + args.extension))

    # Features for the source input utterance
    print("Reading:", args.input_wav)
    input_features = linearvc_model.get_features(args.input_wav)

    # The voice conversion projection matrix
    W = linearvc_model.get_projmat(
        source_wavs,
        target_wavs,
        parallel=args.parallel,
        lasso=args.lasso,
        vad=args.vad,
    )

    # Project the input and vocode
    output_wav = linearvc_model.project_and_vocode(input_features, W)

    print("Writing:", args.output_wav)
    torchaudio.save(args.output_wav, output_wav[None], linearvc_model.sr)


if __name__ == "__main__":
    args = check_argv()
    main(args)
