"""Four named probabilities for the OpenADMET 50 uM CYP activity screen."""

from __future__ import annotations

from typing import Any

SIGNATURE_VERSION = 1
INPUTS = ["smiles"]
ENZYMES = ("1a2", "2c9", "2d6", "3a4")
OUTPUTS: list[dict[str, Any]] = [
    {
        "name": f"cyp{enzyme}_screen50",
        "dtype": "float32",
        "range": [0.0, 1.0],
        "semantics": (
            f"P(CYP{enzyme.upper()} activity reduced at least 50% in the "
            "OpenADMET 50 uM single-concentration assay)"
        ),
        "missing": "NaN when RDKit cannot parse the input SMILES",
    }
    for enzyme in ENZYMES
]


def column_names() -> list[str]:
    return [output["name"] for output in OUTPUTS]


def as_manifest_table() -> dict[str, Any]:
    return {"version": SIGNATURE_VERSION, "inputs": INPUTS, "outputs": OUTPUTS}
