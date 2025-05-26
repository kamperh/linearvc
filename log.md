# Development log

### 2025-01-09

Subjective test:

    # kNN-VC
    mkdir -p ~/Dropbox/temp/julian/speakersim/knnvc/
    cp ~/scratch/knnvc/test-clean/2025-01-13_speakersim/*/*.wav ~/Dropbox/temp/julian/speakersim/knnvc/
    mkdir -p ~/Dropbox/temp/julian/naturalness/knnvc/
    cp ~/scratch/knnvc/test-clean/2025-01-13_naturalness/*/*.wav ~/Dropbox/temp/julian/naturalness/knnvc/

    # FreeVC
    mkdir -p ~/Dropbox/temp/julian/speakersim/freevc/
    cp ~/scratch/freevc/test-clean/speakersim/*/*.wav ~/Dropbox/temp/julian/speakersim/freevc/
    mkdir -p ~/Dropbox/temp/julian/naturalness/freevc/
    cp ~/scratch/freevc/test-clean/naturalness/*/*.wav ~/Dropbox/temp/julian/naturalness/freevc/

    # LinearVC
    mkdir -p ~/Dropbox/temp/julian/speakersim/linearvc/
    cp ~/scratch/linearvc/test-clean/2025-01-13_speakersim/*/*.wav ~/Dropbox/temp/julian/speakersim/linearvc/
    mkdir -p ~/Dropbox/temp/julian/naturalness/linearvc/
    cp ~/scratch/linearvc/test-clean/2025-01-13_naturalness/*/*.wav ~/Dropbox/temp/julian/naturalness/linearvc/

    # Content factorisation
    mkdir -p ~/Dropbox/temp/julian/speakersim/linearvc_contentfact/
    cp ~/scratch/linearvc/test-clean/2025-01-13_speakersim_r100/*/*.wav ~/Dropbox/temp/julian/speakersim/linearvc_contentfact/
    mkdir -p ~/Dropbox/temp/julian/naturalness/linearvc_contentfact/
    cp ~/scratch/linearvc/test-clean/2025-01-13_naturalness_r100/*/*.wav ~/Dropbox/temp/julian/naturalness/linearvc_contentfact/



### 2025-01-07

LinearVC, test-clean excluding evaluation inputs:

    # /home/kamperh/scratch/linearvc/test-clean/2025-01-07

               eer
    mean  0.335769
    std   0.096417

    WER: 4.94% +- 0.07%
    CER: 2.57% +- 0.04%

LinearVC content factorisation r=100, test-clean excluding evaluation inputs:

    # /home/kamperh/scratch/linearvc/test-clean/2025-01-07_fact_r100

               eer
    mean  0.351538
    std   0.094338

    WER: 4.74% +- 0.10%
    CER: 2.51% +- 0.06%

kNN-VC, test-clean excluding evaluation inputs:

    # /home/kamperh/scratch/knnvc/test-clean/2025-01-07

               eer
    mean  0.389231
    std   0.092576

    WER: 5.66% +- 0.08%
    CER: 2.91% +- 0.04%

No constraints with bias, dev-clean excluding evaluation inputs:

    # /home/kamperh/scratch/linearvc/dev-clean/2025-01-07

               eer
    mean  0.318205
    std   0.113962

    WER: 5.48% +- 0.19%
    CER: 3.24% +- 0.19%

No constraints, dev-clean excluding evaluation inputs:

    # /home/kamperh/scratch/linearvc/dev-clean/2025-01-07_without_bias

               eer
    mean  0.317692
    std   0.112952

    WER: 5.43% +- 0.18%
    CER: 3.21% +- 0.18%    

Orthogonal with bias, dev-clean excluding evaluation inputs:

    # /home/kamperh/scratch/linearvc/dev-clean/2025-01-07_procrustes_bias

               eer
    mean  0.282949
    std   0.109766

    WER: 5.02% +- 0.15%
    CER: 2.89% +- 0.14%

Orthogonal without bias, dev-clean excluding evaluation inputs:

    # /home/kamperh/scratch/linearvc/dev-clean/2025-01-07_procrustes
    
               eer
    mean  0.277308
    std   0.109708

    WER: 5.07% +- 0.14%
    CER: 2.92% +- 0.14%

Bias only, dev-clean excluding evaluation inputs:

    # /home/kamperh/scratch/linearvc/dev-clean/2025-01-07_bias

               eer
    mean  0.077436
    std   0.085534

    WER: 5.02% +- 0.14%
    CER: 2.92% +- 0.14%

Content factorisation, dev-clean excluding evaluation inputs, r=6:

    # /home/kamperh/scratch/linearvc/dev-clean/2025-01-07_fact_r6

               eer
    mean  0.003718
    std   0.009646

    WER: 32.20% +- 0.21%
    CER: 19.09% +- 0.13%

Content factorisation, dev-clean excluding evaluation inputs, r=8:

               eer
    mean  0.017564
    std   0.037575

    WER: 16.16% +- 0.18%
    CER: 9.07% +- 0.14%

Content factorisation, dev-clean excluding evaluation inputs, r=12:

               eer
    mean  0.054744
    std   0.078630

    WER: 8.31% +- 0.14%
    CER: 4.55% +- 0.13%

Content factorisation, dev-clean excluding evaluation inputs, r=16:

               eer
    mean  0.099103
    std   0.092850

    WER: 6.36% +- 0.11%
    CER: 3.37% +- 0.09%

Content factorisation, dev-clean excluding evaluation inputs, r=20:
    
               eer
    mean  0.136795
    std   0.102066

    WER: 5.44% +- 0.11%
    CER: 2.82% +- 0.09%    

Content factorisation, dev-clean excluding evaluation inputs, r=24:
    
               eer
    mean  0.168077
    std   0.106793

    WER: 5.17% +- 0.10%
    CER: 2.72% +- 0.08%

Content factorisation, dev-clean excluding evaluation inputs, r=32:

               eer
    mean  0.206154
    std   0.107125

    WER: 5.17% +- 0.11%
    CER: 2.78% +- 0.10%

Content factorisation, dev-clean excluding evaluation inputs, r=48:

               eer
    mean  0.265769
    std   0.111654

    WER: 5.10% +- 0.13%
    CER: 2.91% +- 0.12%

Content factorisation, dev-clean excluding evaluation inputs, r=64:

               eer
    mean  0.291667
    std   0.107828

    WER: 5.30% +- 0.17%
    CER: 3.09% +- 0.17%

Content factorisation, dev-clean excluding evaluation inputs, r=100:

               eer
    mean  0.327564
    std   0.103436

    WER: 5.49% +- 0.16%
    CER: 3.23% +- 0.16%

Content factorisation, dev-clean excluding evaluation inputs, r=128:

               eer
    mean  0.343205
    std   0.103808

    WER: 5.64% +- 0.17%
    CER: 3.35% +- 0.17%

Content factorisation, dev-clean excluding evaluation inputs, r=192:

               eer
    mean  0.345128
    std   0.105419

    WER: 6.44% +- 0.14%
    CER: 3.60% +- 0.14%

Content factorisation, dev-clean excluding evaluation inputs, r=224:

               eer
    mean  0.328974
    std   0.106452

    WER: 7.56% +- 0.12%
    CER: 4.09% +- 0.11%

Content factorisation, dev-clean excluding evaluation inputs, r=256:

               eer
    mean  0.303718
    std   0.107905

    WER: 10.02% +- 0.13%
    CER: 5.41% +- 0.10%


### 2024-12-10

LibriSpeech test-clean using content factorisation, r=100 *select*:

               eer
    mean  0.350641
    std   0.090788

    WER: 4.75% +- 0.06%
    CER: 2.48% +- 0.03%

LibriSpeech dev-clean using content factorisation, r=4, add:

          eer
    mean  0.0
    std   0.0

    WER: 102.31% +- 0.56%
    CER: 78.55% +- 0.46%

LibriSpeech dev-clean using content factorisation, r=6:

               eer
    mean  0.003462
    std   0.009881

    WER: 32.30% +- 0.20%
    CER: 19.23% +- 0.13%

LibriSpeech dev-clean using content factorisation, r=8:

               eer
    mean  0.016795
    std   0.037071

    WER: 16.21% +- 0.16%
    CER: 9.12% +- 0.12%

LibriSpeech dev-clean using content factorisation, r=12, add:

               eer
    mean  0.054615
    std   0.077691

    WER: 8.32% +- 0.13%
    CER: 4.51% +- 0.12%

LibriSpeech dev-clean using content factorisation, r=16:

               eer
    mean  0.098718
    std   0.093330

    WER: 6.39% +- 0.12%    
    CER: 3.43% +- 0.10%    

LibriSpeech dev-clean using content factorisation, r=32:

               eer
    mean  0.205769
    std   0.106955

    WER: 5.17% +- 0.12%    
    CER: 2.80% +- 0.10%

LibriSpeech dev-clean using content factorisation, r=48:

               eer
    mean  0.265000
    std   0.110729

    WER: 4.98% +- 0.12%
    CER: 2.76% +- 0.11%

LibriSpeech dev-clean using content factorisation, r=64:

               eer
    mean  0.289487
    std   0.107262

    WER: 5.23% +- 0.15%
    CER: 3.02% +- 0.15%

LibriSpeech dev-clean using content factorisation, r=96:

               eer
    mean  0.323846
    std   0.101676

    WER: 5.30% +- 0.16%
    CER: 3.08% +- 0.15%

LibriSpeech dev-clean using content factorisation, r=100 *select*:

               eer
    mean  0.325641
    std   0.099609

    WER: 5.38% +- 0.16%
    CER: 3.13% +- 0.15%

LibriSpeech dev-clean using content factorisation, r=128:

               eer
    mean  0.339744
    std   0.102339

    WER: 5.60% +- 0.17%
    CER: 3.28% +- 0.17%

LibriSpeech dev-clean using content factorisation, r=192:

               eer
    mean  0.343974
    std   0.101489

    WER: 6.38% +- 0.13%
    CER: 3.51% +- 0.12%

LibriSpeech dev-clean using content factorisation, r=224, add:

               eer
    mean  0.330128
    std   0.106377

    WER: 7.76% +- 0.13%
    CER: 4.23% +- 0.12%

LibriSpeech dev-clean using content factorisation, r=256:

               eer
    mean  0.305513
    std   0.108082

    WER: 10.09% +- 0.15%
    CER: 5.49% +- 0.13%


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
