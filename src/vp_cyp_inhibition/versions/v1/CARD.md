# cyp-inhibition v1

_Generated from `manifest.toml` and `metrics.json`. Do not edit._

Released 2026-09-27 · signature 1

**Why this version.** First four-enzyme 50 uM CYP activity screen release

## Outputs

| column | dtype | range | meaning |
|---|---|---|---|
| `cyp1a2_screen50` | float32 | 0.0–1.0 | P(CYP1A2 activity reduced at least 50% in the OpenADMET 50 uM single-concentration assay) |
| `cyp2c9_screen50` | float32 | 0.0–1.0 | P(CYP2C9 activity reduced at least 50% in the OpenADMET 50 uM single-concentration assay) |
| `cyp2d6_screen50` | float32 | 0.0–1.0 | P(CYP2D6 activity reduced at least 50% in the OpenADMET 50 uM single-concentration assay) |
| `cyp3a4_screen50` | float32 | 0.0–1.0 | P(CYP3A4 activity reduced at least 50% in the OpenADMET 50 uM single-concentration assay) |

Missing values: NaN when RDKit cannot parse the input SMILES

## Performance

Protocol `scaffold-balanced-5seed@1` — Bemis-Murcko scaffold split with scaffold groups permuted by seed and each group placed in the fold it overfills least, so a group larger than a fold's capacity settles in train instead of starving that fold. Same fold fractions, seeds and metrics as scaffold-shuffle-5seed@1; only the packing differs. Five seeds; report mean and standard deviation over the held-out test folds.

Evaluated 2026-09-27 on n_train=3281, n_val=437, n_test=656.

### `cyp1a2_screen50`

| metric | mean | std | per seed |
|---|---|---|---|
| auc_roc | 0.805 | 0.016 | 0.830, 0.804, 0.810, 0.779, 0.804 |
| auprc | 0.639 | 0.033 | 0.683, 0.648, 0.657, 0.584, 0.624 |
| mcc | 0.421 | 0.041 | 0.476, 0.444, 0.429, 0.353, 0.404 |
| brier | 0.153 | 0.007 | 0.148, 0.149, 0.149, 0.166, 0.152 |

### `cyp2c9_screen50`

Measured on n_train=3281, n_val=437, n_test=656.

| metric | mean | std | per seed |
|---|---|---|---|
| auc_roc | 0.839 | 0.009 | 0.849, 0.843, 0.837, 0.840, 0.823 |
| auprc | 0.732 | 0.014 | 0.729, 0.753, 0.730, 0.739, 0.711 |
| mcc | 0.479 | 0.030 | 0.445, 0.501, 0.514, 0.493, 0.441 |
| brier | 0.151 | 0.002 | 0.150, 0.149, 0.152, 0.152, 0.153 |

### `cyp2d6_screen50`

Measured on n_train=3281, n_val=437, n_test=656.

| metric | mean | std | per seed |
|---|---|---|---|
| auc_roc | 0.808 | 0.008 | 0.801, 0.823, 0.810, 0.802, 0.805 |
| auprc | 0.646 | 0.024 | 0.650, 0.649, 0.672, 0.600, 0.658 |
| mcc | 0.406 | 0.058 | 0.380, 0.472, 0.475, 0.328, 0.376 |
| brier | 0.150 | 0.008 | 0.155, 0.138, 0.142, 0.156, 0.157 |

### `cyp3a4_screen50`

Measured on n_train=3281, n_val=437, n_test=656.

| metric | mean | std | per seed |
|---|---|---|---|
| auc_roc | 0.847 | 0.010 | 0.838, 0.845, 0.840, 0.867, 0.846 |
| auprc | 0.919 | 0.008 | 0.917, 0.919, 0.917, 0.932, 0.908 |
| mcc | 0.493 | 0.040 | 0.450, 0.474, 0.470, 0.563, 0.507 |
| brier | 0.146 | 0.007 | 0.151, 0.146, 0.151, 0.133, 0.148 |

> Comparable only with metrics carrying the same protocol id.

## Data

OpenADMET CYP challenge 50 uM activity screen — Pinned single-concentration training table; log2 fold change <= -1. Retrieved 2026-09-27, licensed Apache-2.0, redistributed here.

`4374` compounds, positive rate `0.299`, table SHA-256 `f2183f3587976259…`

Regenerate and check for upstream drift with `python -m vp_cyp_inhibition.data fetch --verify`.

## Model

xgboost-binary on `morgan2_1024_openadmet10` features. Shipped weights: one fixed-recipe estimator per output on all labeled compounds

`weights.joblib` SHA-256 `220f0c1493779689…`

## Provenance

Environment: python 3.12.9, rdkit 2026.03.6, sklearn 1.9.1, xgboost 3.4.1.

Reproducibility is to this dataset hash and this environment, not bit-exact: the sources are live endpoints and RDKit descriptor values move between releases.
