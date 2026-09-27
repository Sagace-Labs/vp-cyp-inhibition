"""Fetch and standardize the pinned OpenADMET four-enzyme screen."""

from __future__ import annotations

import argparse
import hashlib
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen

import pandas as pd

from vp_core import dataset
from vp_core.standardise import standardise_many

ROOT = Path(__file__).resolve().parents[2]
TABLE_PATH = ROOT / "data/cyp_inhibition.parquet"
EXAMPLE_PATH = ROOT / "data/example/cyp_inhibition_example.parquet"
REVISION = "146282d2ce1532f1803679a834a9bec9dac1e482"
FILENAME = "cyp-challenge-single-concentration-TRAIN.csv"
RAW_SHA256 = "cf275440aa33d10b16e7a3a19f1b196d59dc379052175ab79b47ca43db663c7a"
ENZYMES = ("1A2", "2C9", "2D6", "3A4")
LABELS = ("label", "cyp2c9", "cyp2d6", "cyp3a4")
OUTPUT_LABELS = {
    f"cyp{enzyme.lower()}_screen50": label
    for enzyme, label in zip(ENZYMES, LABELS, strict=True)
}
MANIFEST_DATA = {
    "name": "OpenADMET CYP challenge 50 uM activity screen",
    "source": "Pinned single-concentration training table; log2 fold change <= -1",
    "url": f"https://huggingface.co/datasets/openadmet/cyp-challenge-train-test/tree/{REVISION}",
    "retrieved": "2026-09-27",
    "licence": "Apache-2.0",
    "redistributable": True,
    "path": "data/cyp_inhibition.parquet",
    "fetch": "python -m vp_cyp_inhibition.data fetch --verify",
}


def _one_enzyme(raw: pd.DataFrame, enzyme: str, label: str) -> pd.DataFrame:
    source = raw.loc[raw.enzyme.eq(f"CYP{enzyme}")].dropna(
        subset=["SMILES", "log2fc_estimate"]
    ).copy()
    smiles, keys = standardise_many(source.SMILES.astype(str).tolist())
    frame = pd.DataFrame({
        "inchikey": keys,
        "smiles": smiles,
        "activity": pd.to_numeric(source.log2fc_estimate, errors="coerce").to_numpy(),
    }).dropna()
    conflicting = frame.groupby("inchikey").activity.nunique()
    frame = frame[~frame.inchikey.isin(conflicting.index[conflicting > 1])]
    frame = frame.drop_duplicates("inchikey")
    frame[label] = (frame.activity <= -1.0).astype("Int64")
    return frame[["inchikey", "smiles", label]]


def standard_table(raw: pd.DataFrame) -> pd.DataFrame:
    """Preserve unmeasured CYP labels as missing, never as inactive."""
    tables = [
        _one_enzyme(raw, enzyme, label)
        for enzyme, label in zip(ENZYMES, LABELS, strict=True)
    ]
    table = tables[0]
    for extra in tables[1:]:
        table = table.merge(extra.drop(columns="smiles"), on="inchikey", how="outer")
    structures = pd.concat([part[["inchikey", "smiles"]] for part in tables])
    structures = structures.drop_duplicates("inchikey")
    table = table.drop(columns="smiles").merge(structures, on="inchikey", how="left")
    table = table[["inchikey", "smiles", *LABELS]].sort_values("inchikey").reset_index(drop=True)
    for label in LABELS:
        table[label] = table[label].astype("Int64")
    errors = dataset.validate_table(table, labels=LABELS)
    if errors:
        raise ValueError("; ".join(errors))
    return table


def load() -> pd.DataFrame:
    if not TABLE_PATH.exists():
        raise FileNotFoundError(f"Missing {TABLE_PATH}; run python -m vp_cyp_inhibition.data fetch")
    return dataset.read_table(TABLE_PATH, labels=LABELS)


def example() -> pd.DataFrame:
    return dataset.read_table(EXAMPLE_PATH, labels=LABELS)


def fetch(*, verify: bool = False) -> pd.DataFrame:
    """Explicitly download the pinned raw file and rebuild the release table."""
    url = f"https://huggingface.co/datasets/openadmet/cyp-challenge-train-test/resolve/{REVISION}/{FILENAME}"
    with urlopen(url, timeout=90) as response:
        body = response.read()
    digest = hashlib.sha256(body).hexdigest()
    if digest != RAW_SHA256:
        raise ValueError(f"OpenADMET source drift: expected {RAW_SHA256}, got {digest}")
    table = standard_table(pd.read_csv(BytesIO(body)))
    if verify:
        from vp_cyp_inhibition import get

        expected = get().manifest["dataset"]["sha256"]
        actual = dataset.dataset_hash(table, labels=LABELS)
        if actual != expected:
            raise ValueError(f"Standardized table drift: {expected} != {actual}")
    dataset.write_table(table, TABLE_PATH, labels=LABELS)
    return table


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["fetch", "verify", "build-example"])
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.command == "fetch":
        table = fetch(verify=args.verify)
    elif args.command == "build-example":
        table = dataset.stratified_example(load(), n=250, labels=LABELS)
        dataset.write_table(table, EXAMPLE_PATH, labels=LABELS)
    else:
        from vp_cyp_inhibition import get

        table = load()
        actual = dataset.dataset_hash(table, labels=LABELS)
        expected = get().manifest["dataset"]["sha256"]
        if actual != expected:
            raise ValueError(f"Standardized table drift: {expected} != {actual}")
    print(len(table))


if __name__ == "__main__":
    main()
