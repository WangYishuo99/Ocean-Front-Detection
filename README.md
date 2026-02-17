# GBM: Gradient-Bayesian-Morphology Framework

Official implementation of:

W. Wang et al.,  
**GBM: An Ocean Front Detection Framework**,  
IEEE Transactions on Geoscience and Remote Sensing, 2026.  
DOI: 10.1109/TGRS.2026.3660295  

---

## Overview

GBM (Gradient-Bayesian-Morphology) is a physically informed and fully interpretable framework for ocean front detection.

The framework integrates three complementary components:

- **Gradient-based thresholding** with physically meaningful priors emphasizing sharp field transitions  
- **Bayesian inference** that combines gradient priors with local field descriptors for adaptive, data-driven frontal classification  
- **Morphological and graph-based refinement** procedures to enforce topological consistency by thinning frontal zones, merging fragmented segments, and removing spurious ring structures  

The proposed method suppresses over-detection, reduces false positives, and improves spatial continuity while maintaining robustness, reproducibility, and physical interpretability.

---

## Key Features

- Physically guided gradient prior
- Adaptive Bayesian classification without fixed threshold tuning
- Morphological thinning and fragment merging
- Systematic removal of spurious ring structures
- Stable performance across weak and strong frontal regimes

---

## Data

The framework was evaluated using daily:

- Sea Surface Temperature (SST)
- Sea Surface Salinity (SSS)

over:

- South China Sea (weak frontal regime)
- Kuroshio region (strong frontal regime)

---

## Requirements

- Python 3.9+
- NumPy
- SciPy
- NetworkX
- Matplotlib

(Additional dependencies may be specified in `requirements.txt`.)

---

## Usage

Example:

```bash
python main.py
```

Configuration details can be modified in the corresponding configuration files.

## Citation

If you find this work useful, please cite:

W. Wang et al.,
"GBM: An Ocean Front Detection Framework,"
IEEE Transactions on Geoscience and Remote Sensing, 2026.
DOI: 10.1109/TGRS.2026.3660295

## Contact

For questions, suggestions, or collaboration:

Please contact: wys1998@sjtu.edu.cn
