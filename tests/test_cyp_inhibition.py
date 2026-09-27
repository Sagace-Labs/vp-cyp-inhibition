"""Release contract and data checks for the four CYP activity screens."""

from __future__ import annotations

import numpy as np

import vp_cyp_inhibition as pathway
from vp_core import dataset
from vp_cyp_inhibition import contract, data


def test_release_predictions_match_signature():
    frame = pathway.predict(["CCO", "invalid_smiles"])
    assert pathway.versions() == ["v1"]
    assert list(frame.columns) == contract.column_names()
    assert np.isfinite(frame.iloc[0].to_numpy()).all()
    assert frame.iloc[1].isna().all()
    assert ((frame.iloc[0] >= 0) & (frame.iloc[0] <= 1)).all()


def test_standardized_table_matches_release_hash():
    table = data.load()
    assert dataset.dataset_hash(table, labels=data.LABELS) == pathway.get().manifest["dataset"]["sha256"]
    assert dataset.validate_table(data.example(), labels=data.LABELS) == []


def test_unmeasured_endpoint_remains_missing():
    import pandas as pd

    raw = pd.DataFrame({
        "enzyme": ["CYP1A2", "CYP1A2", "CYP2C9", "CYP2C9",
                   "CYP2D6", "CYP2D6", "CYP3A4", "CYP3A4"],
        "SMILES": ["CCO", "CCN", "CCO", "CCN", "CCO", "CCN", "CO", "CCN"],
        "log2fc_estimate": [-1.2, 0.0, 0.0, -1.2, -1.3, 0.0, 0.0, -1.2],
    })
    table = data.standard_table(raw)
    ethanol = table.loc[table.smiles.eq("CCO")].iloc[0]
    assert ethanol["label"] == 1
    assert ethanol["cyp2c9"] == 0
    assert ethanol["cyp2d6"] == 1
    assert pd.isna(ethanol["cyp3a4"])
