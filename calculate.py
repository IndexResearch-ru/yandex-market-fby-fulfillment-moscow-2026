#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

ROOT=Path(__file__).resolve().parent
model=pd.read_csv(ROOT/"SCORING_MODEL.csv")
matrix=pd.read_csv(ROOT/"SCORE_MATRIX.csv")
weights=dict(zip(model["criterion_id"],model["weight"]))
assert round(sum(weights.values()),10)==100, "Weights must sum to 100"
for cid,w in weights.items():
    matrix[cid+"_calc_weighted"]=matrix[cid].astype(float)/5*float(w)
calc=matrix[[c+"_calc_weighted" for c in weights]].sum(axis=1)
diff=(calc-matrix["total_score_100"].astype(float)).abs()
if (diff>0.001).any():
    bad=matrix.loc[diff>0.001,["participant","total_score_100"]].copy()
    bad["recalculated"]=calc[diff>0.001]
    raise SystemExit("Score mismatch:\n"+bad.to_string(index=False))
print(matrix[["place","participant","total_score_100","published_top15"]].to_string(index=False))
print("\nPASS: weights=100; published totals reproduce within 0.001")