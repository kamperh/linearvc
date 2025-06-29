# LinearVC: Linear transformations of self-supervised features through the lens of voice conversion

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](license.md)
[![paper](https://img.shields.io/badge/Paper-arXiv-red.svg)](https://arxiv.org/abs/2506.01510)
[![colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kamperh/linearvc/blob/master/demo.ipynb)


## Overview

Voice conversion is performed using just linear regression. The work is described in:

- H. Kamper, B. van Niekerk, J. Zaïdi, and M-A. Carbonneau, "LinearVC: Linear transformations of self-supervised features through the lens of voice conversion," in *Interspeech*, 2025.

Samples: <https://www.kamperh.com/linearvc/>


## Quick start

### Programmatic usage

Install the dependencies in `environment.yml` or run `conda env create -f environment.yml` and check that everything installed correctly. The steps below are also illustrated in the [demo notebook](demo.ipynb).

```Python
import torch
import torchaudio

device = "cuda"  # "cpu"

# Load all the required models
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
linearvc_model = linearvc.LinearVC(wavlm, hifigan, device)

# Lists of source and target audio files
source_wavs = [
    "<filename of audio from source speaker 1>.wav",
    "<filename of audio from source speaker 2>.wav",
    ...,
]
target_wavs = [
    "<filename of audio from target speaker 1>.wav",
    "<filename of audio from target speaker 2>.wav",
    ...,
]

# Source input utterance
input_features = linearvc_model.get_features("<filename>.wav")

# Voice conversion projection matrix
W = linearvc_model.get_projmat(
    source_wavs,
    target_wavs,
    parallel=True,  # enable if parallel
    vad=False,
)

# Project the input and vocode
output_wav = linearvc_model.project_and_vocode(input_features, W)
torchaudio.save("output.wav", output_wav[None], 16000)
```

If `parallel=True`, utterances with the same filename are paired up. If `parallel=False`, the utterances don't have to align, but then you need more data (3 minutes per speaker is good, more than that doesn't help much).


### Script usage

Perform LinearVC by finding all the source and target audio files in given directories:

    ./linearvc.py \
        --extension .flac \
        ~/LibriSpeech/dev-clean/1272/ \
        ~/LibriSpeech/dev-clean/1462/ \
        ~/LibriSpeech/dev-clean/1272/128104/1272-128104-0000.flac \
        output.wav

When parallel utterances are available, much less data is needed. Running the script with `--parallel` as below scans two directories and pairs up all utterances with the same filename. E.g. below it finds `002.wav`, `003.wav`, etc. in the `p225/` source directory and then pairs these up with the same filenames in the `p226/` directory.

    ./linearvc.py \
        --parallel \
        data/vctk_demo/p225/ \
        data/vctk_demo/p226/ \
        data/vctk_demo/p225/067.wav \
        output2.wav

Full script details:

```
usage: linearvc.py [-h] [--parallel] [--lasso LASSO] [--vad]
                   [--extension {.flac,.wav}]
                   source_wav_dir target_wav_dir input_wav output_wav

Perform voice conversion with linear regression.

positional arguments:
  source_wav_dir        directory with source speaker speech
  target_wav_dir        directory with target speaker speech
  input_wav             input speech filename
  output_wav            output speech filename

options:
  -h, --help            show this help message and exit
  --parallel            whether source and target utterances are parallel, in
                        which case the filenames in the two directories should
                        match
  --lasso LASSO         lasso is applied with this alpha value
  --vad                 voice activatiy detecion is applied to start of
                        utterance
  --extension {.flac,.wav}
                        source and target audio file extension (default:
                        '.wav')
```


## Experiments on all utterances (LibriSpeech)

These experiments are described in ([Kamper et al. 2025](https://arxiv.org/abs/2506.01510)).

Extract WavLM features:

    ./extract_wavlm_libri.py \
        --exclude data/eval_inputs_dev-clean.txt \
        ~/endgame/datasets/librispeech/LibriSpeech/dev-clean/ \
        ~/scratch/dev-clean/wavlm_exclude/
    ./extract_wavlm_libri.py \ 
        --exclude data/eval_inputs_test-clean.txt \
        ~/endgame/datasets/librispeech/LibriSpeech/test-clean/ \
        ~/scratch/test-clean/wavlm_exclude/

Experiments with all utterances:

    jupyter lab experiments_libri.ipynb


## Experiments on parallel utterances (VCTK)

These experiments are not described in the paper but are still interesting.

Downsample speech to 16kHz:

    # Development set
    ./resample_vad.py \
        data/vctk_scottish.txt \
        ~/endgame/datasets/VCTK-Corpus/wav48/ \
        ~/scratch/vctk/wav/scottish/

    # Test set
    ./resample_vad.py \
        data/vctk_english.txt \
        ~/endgame/datasets/VCTK-Corpus/wav48/ \
        ~/scratch/vctk/wav/english/

Create the evaluation dataset (which is already in the `data/` directory released with the repo):

    ./evalcsv_vctk.py \
        data/vctk_scottish.txt \
        /home/kamperh/scratch/vctk/wav/scottish/ \
        data/speakersim_vctk_scottish_2024-09-16.csv
    ./evalcsv_vctk.py \
        data/vctk_english.txt \
        /home/kamperh/scratch/vctk/wav/english/ \
        data/speakersim_vctk_english_2024-09-16.csv

Extract features for particular parallel utterances (for baselines):

    ./extract_wavlm_vctk.py --utterance 008 \
        ~/scratch/vctk/wav/english/ ~/scratch/vctk/english/wavlm_008/

Experiments with parallel utterances:

    jupyter lab experiments_vctk.ipynb

