"""Measure the inhibition release under its registered protocol."""

from __future__ import annotations

import argparse

from vp_core.binary_panel import evaluate_version
from vp_cyp_inhibition import PATHWAY, current_version, data, get, model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", default=None)
    parser.add_argument("--protocol", default=None)
    parser.add_argument("--example", action="store_true")
    args = parser.parse_args()
    record = evaluate_version(
        PATHWAY, get, data, model, args.version or current_version(),
        protocol_id=args.protocol, use_example=args.example, write=not args.example,
    )
    print(record["test"])


if __name__ == "__main__":
    main()
