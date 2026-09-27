# vp-cyp-inhibition

Predicts activity reduction in four CYP enzymes from a SMILES string.

## Install

    pip install vp-cyp-inhibition

## Use

    from vp_cyp_inhibition import predict
    predict(["CC(=O)Oc1ccccc1C(=O)O"])
    # -> DataFrame[cyp1a2_screen50, cyp2c9_screen50,
    #              cyp2d6_screen50, cyp3a4_screen50]

Each column is a probability for the specified 50 µM in vitro activity screen.
Invalid SMILES yield NaN. Pin the model with `version="v1"`.

## Current version

**v1**, signature 1, evaluated under `scaffold-balanced-5seed@1`. Per-enzyme
metrics, fold sizes and standard deviations are in
[`src/vp_cyp_inhibition/versions/v1/CARD.md`](src/vp_cyp_inhibition/versions/v1/CARD.md).

## Data

The four outputs use the pinned OpenADMET single-concentration CYP challenge
training table, binarized at at least 50% activity reduction. The standardized
table and a small example fixture are under `data/`; rebuild with
`python -m vp_cyp_inhibition.data fetch --verify`. See [`data/README.md`](data/README.md).

## Retrain

    python -m vp_cyp_inhibition.train --version v2 --reason "why this version exists"
    python -m vp_cyp_inhibition.evaluate --version v2

`train` creates new immutable weights; `evaluate` refits on the registered
scaffold folds and regenerates the card.

## Licence

Code is Apache-2.0 ([`LICENSE`](LICENSE)); bundled data are Apache-2.0
([`LICENSE-DATA`](LICENSE-DATA)).

## Cite

See [`CITATION.cff`](CITATION.cff).
