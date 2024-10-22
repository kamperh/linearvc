# LinearVC: Voice conversion with just linear regression

To-do:

- Jupyter notebook link
- arXiv link (see Simon)
- license link


## Quick start

### Programmatic usage

Install the dependencies in `environment.yml` or run
`conda env create -f environment.yml` and check that everything install
correctly.

To-do: HERE! Check `demo.ipynb`


### Script usage

Perform LinearVC by reading all the source and target audio files in given
directories:

    ./linearvc.py \
        --extension .flac \
        ~/LibriSpeech/dev-clean/1272/ \
        ~/LibriSpeech/dev-clean/1462/ \
        ~/LibriSpeech/dev-clean/1272/128104/1272-128104-0000.flac \
        output.wav

When parallel utterances are available, much less data is needed. The script
with `--parallel` scans two directories and pairs up all utterances with the
same filename. E.g. below it finds `002.wav`, `003.wav`, etc. in the `p225/`
source directory and then pairs these up with the same filenames in the `p226/`
directory.

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



**to-do** Add easy notebook and usage from TorchHub:

- For full LinearVC, similar to kNN-VC
- For LinearVC with multiple parallel utterances


## Experiments on all utterances (LibriSpeech)

Extract original WavLM features:

    ./extract_wavlm_libri.py \
        ~/endgame/datasets/librispeech/LibriSpeech/test-clean/ \
        ~/scratch/test-clean/wavlm/

Experiments with all utterances:

    jupyter lab experiments_full.ipynb


## Experiments on parallel utterances (English-accented VCTK)

Downsample speech to 16kHz:

    ./resample_vad.py ~/endgame/datasets/VCTK-Corpus/wav48 ~/scratch/vctk/wav

Create the evaluation dataset (which is already in the `data` directory released
with the repo):

    ./evalcsv_vctk.py data/speakersim_vctk_english_2024-09-16.csv

Extract features for particular parallel utterances (for baselines):

    ./extract_wavlm.py --utterance 008 \
        ~/scratch/vctk/wav ~/scratch/vctk/wavlm_008

Experiments with parallel utterances:

    jupyter lab experiments_vctk.ipynb


## Results

With all utterances we get the following results.



With one parallel utterance we get the following results.

LinearVC:

               eer
    mean  0.314409
    std   0.083072

    WER: 7.58% +- 0.22%
    CER: 6.93% +- 0.12%

kNN-VC:

               eer
    mean  0.353763
    std   0.079758

    WER: 27.37% +- 0.45%
    CER: 19.18% +- 0.29%

