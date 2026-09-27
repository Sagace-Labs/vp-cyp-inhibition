"""Fixed Morgan-and-descriptor XGBoost recipe for the 50 uM screen."""

from __future__ import annotations

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier

FEATURES = "morgan2_1024_openadmet10"
FEATURES_BY_OUTPUT: dict[str, str] = {}
FAMILY = "xgboost-binary"


def features_for(output: str) -> str:
    return FEATURES_BY_OUTPUT.get(output, FEATURES)


def fit(X, y, *, output: str, seed: int):
    transform = ColumnTransformer(
        [("descriptors", StandardScaler(), list(range(1024, 1034)))],
        remainder="passthrough",
    )
    classifier = XGBClassifier(
        n_estimators=220,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=5,
        tree_method="hist",
        n_jobs=4,
        random_state=seed,
        eval_metric="logloss",
    )
    return Pipeline([("scale", transform), ("classifier", classifier)]).fit(X, y)


def predict_proba(fitted, X):
    return fitted.predict_proba(X)[:, 1]
