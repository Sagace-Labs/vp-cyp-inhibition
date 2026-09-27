"""Create an immutable four-enzyme inhibition release."""

from __future__ import annotations

import argparse

from vp_core.binary_panel import build_version
from vp_cyp_inhibition import PATHWAY, VERSIONS_DIR, contract, data, model


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True)
    parser.add_argument("--reason", required=True)
    args = parser.parse_args()
    print(build_version(PATHWAY, VERSIONS_DIR, contract, data, model, args.version, reason=args.reason))


if __name__ == "__main__":
    main()
