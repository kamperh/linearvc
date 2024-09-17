# LinearVC: Voice conversion with just linear regression


## Minimal example

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

