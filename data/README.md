# CYP inhibition table

`cyp_inhibition.parquet` holds one standardized compound per InChIKey, with
four nullable binary labels. Null means that enzyme has no retained readout.
`label` is CYP1A2; the other columns are `cyp2c9`, `cyp2d6`, `cyp3a4`.
The label is 1 when the pinned 50 µM assay has `log2fc_estimate <= -1`.
Conflicting duplicate continuous readouts are dropped before binarization.
`example/` is a small stratified fixture for package tests.
