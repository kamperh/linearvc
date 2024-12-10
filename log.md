# Development log

### 2024-12-10

LibriSpeech dev-clean using content factorisation, r=64:




### 2024-12-06

LibriSpeech dev-clean subset using SVD basis:

               eer
    mean  0.334359
    std   0.131732

    WER: 5.12% +- 0.27%
    CER: 2.58% +- 0.13%

LibriSpeech dev-clean subset using "old" LinearVC:

               eer
    mean  0.331795
    std   0.105064

    WER: 5.34% +- 0.29%
    CER: 2.55% +- 0.12%

LibriSpeech, bias-only:

               eer
    mean  0.077692
    std   0.086458

    WER: 5.09% +- 0.16%
    CER: 2.99% +- 0.16%


### 2024-11-18

VCTK, scottish, lasso=0.4:

    EER: 0.307018 +- 0.05279

    WER: 7.47% +- 0.36%
    CER: 6.58% +- 0.19%

VCTK, scottish, orthogonal_procrustes:

               eer
    mean  0.336842
    std   0.058801

    WER: 10.83% +- 0.44%
    CER: 8.60% +- 0.26%

VCTK, scottish, additive:

               eer
    mean  0.204678
    std   0.066079

    WER: 4.80% +- 0.26%
    CER: 4.91% +- 0.14%

VCTK, scottish, groundtruth:

    WER: 4.13% +- 1.19%
    CER: 4.67% +- 0.66%


### 2024-11-13

LibriSpeech, alpha=3.0:

    # /home/kamperh/scratch/linearvc/dev-clean/2024-11-12_lasso3.0
               
               eer
    mean  0.046026
    std   0.074979

    WER: 5.41% +- 0.11%
    CER: 2.99% +- 0.10%

LibriSpeech, alpha=0.3:

    # /home/kamperh/scratch/linearvc/dev-clean/2024-11-12_lasso0.3

               eer
    mean  0.194231
    std   0.113916

    WER: 4.89% +- 0.12%
    CER: 2.72% +- 0.11%

LibriSpeech, alpha=0.4:

    # /home/kamperh/scratch/linearvc/dev-clean/2024-11-12_lasso0.4

               eer
    mean  0.176282
    std   0.109882

    WER: 4.91% +- 0.12%
    CER: 2.71% +- 0.11%

LibriSpeech, lstsq:

    # /home/kamperh/scratch/linearvc/dev-clean/2024-11-13_noreg

               eer
    mean  0.316667
    std   0.112867

    WER: 5.42% +- 0.18%
    CER: 3.18% +- 0.18%

LibriSpeech, LinearRegression with bias:

    # /home/kamperh/scratch/linearvc/dev-clean/2024-12-04_linear_bias

               eer
    mean  0.317564
    std   0.112901

    WER: 5.43% +- 0.18%
    CER: 3.20% +- 0.18%


LibriSpeech, orthogonal_procrustes with bias:

    # /home/kamperh/scratch/linearvc/dev-clean/2024-12-04_procrustes_bias

               eer
    mean  0.285513
    std   0.110376

    WER: 5.17% +- 0.16%
    CER: 3.03% +- 0.16%

LibriSpeech, orthogonal_procrustes:

    # /home/kamperh/scratch/linearvc/dev-clean/2024-11-13_procrus

               eer
    mean  0.280385
    std   0.109738

    WER: 5.24% +- 0.17%
    CER: 3.09% +- 0.16%

LibriSpeech, additive:

    # /home/kamperh/scratch/linearvc/dev-clean/2024-11-13_add

               eer
    mean  0.072564
    std   0.084173

    WER: 5.26% +- 0.17%
    CER: 3.14% +- 0.17%
