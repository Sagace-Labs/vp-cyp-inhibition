"""Predict activity reduction in four OpenADMET CYP screens from SMILES."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from vp_core.binary_panel import predict_values
from vp_core.registry import Version, VersionedPathway
from vp_cyp_inhibition import model

__version__ = "1.0.0"
PATHWAY = "cyp-inhibition"
VERSIONS_DIR = Path(__file__).resolve().parent / "versions"


def _predict(fitted, smiles: list[str], version: Version):
    return predict_values(fitted, smiles, version, model)


_pathway = VersionedPathway(PATHWAY, VERSIONS_DIR, predict_fn=_predict)


def predict(smiles: list[str], *, version: str | None = None) -> pd.DataFrame:
    return _pathway.predict(smiles, version=version)


def versions() -> list[str]:
    return _pathway.versions()


def current_version() -> str:
    return _pathway.current()


def get(version: str | None = None) -> Version:
    return _pathway.get(version)


def signature(version: str | None = None) -> dict[str, Any]:
    return get(version).manifest["signature"]
