# LinearVC: Voice conversion with just linear regression


## Minimal example

**to-do** Add easy notebook and usage from TorchHub:

- For full LinearVC, similar to kNN-VC
- For LinearVC with multiple parallel utterances


## Experiments with all utterances from English-accented speakers

Downsample speech to 16kHz:

    ./resample_vad.py ~/endgame/datasets/VCTK-Corpus/wav48/ ~/scratch/vctk/wav/

Create the evaluation dataset (which is already in the `data` directory released
with the repo):

    ./evalcsv_vctk.py data/speakersim_vctk_english_2024-09-16.csv




## Experiments with only parallel utterance(s)




