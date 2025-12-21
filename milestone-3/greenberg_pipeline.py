from __future__ import annotations

from typing import Callable, List, Dict, Any
import numpy as np
import pandas as pd
import plotly.express as px

# -------------------------
# Data preparation utilities
# -------------------------
def features_to_df(features_dict: Dict[str, Any]) -> pd.DataFrame:
    """
    Convert Lang2Vec feature dict to a pandas DataFrame.
    Lang2Vec uses '--' for missing values -> converted to np.nan.
    The DataFrame index is language code; caller may reset_index later.
    """
    cols = features_dict["CODE"]
  
    rows = []
    idx = []
    for lang, vals in features_dict.items():
        if lang == "CODE":
            continue
        rows.append(vals)
        idx.append(lang)

    df = pd.DataFrame(rows, index=idx, columns=cols)

    df = df.replace("--", np.nan)
    return df

def prepare_wals_coords(wals_languages_csv_path: str) -> pd.DataFrame:
    """
    Load WALS language metadata and return normalized coordinates table.

    Output columns:
      - lang_code, latitude, longitude, macro_area, family, language_name
    """
    wals_langs = pd.read_csv(wals_languages_csv_path)

    coords = (
        wals_langs[["ISO639P3code", "Latitude", "Longitude", "Macroarea", "Family", "Name"]]
        .dropna(subset=["Latitude", "Longitude"])
        .rename(columns={
            "ISO639P3code": "lang_code",
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Macroarea": "macro_area",
            "Family": "family",
            "Name": "language_name",
        })
    )
    coords["lang_code"] = coords["lang_code"].astype(str)
    return coords

def normalize_lang2vec_syntax_df(
    df: pd.DataFrame,
    rule_features_needed: List[str]
    ) -> pd.DataFrame:
    """
    Normalize Lang2Vec syntax features for a specific rule.

    - Ensures a lang_code column exists
    - Restricts columns to lang_code + rule-relevant features
    """
    out = df.copy()

    # Lang2Vec often uses language code as index
    if "lang_code" not in out.columns:
        out = out.reset_index().rename(columns={"index": "lang_code"})

    out["lang_code"] = out["lang_code"].astype(str)

    # Optional: keep only columns we need + lang_code (avoids huge tables downstream)
    keep_cols = ["lang_code"] + [c for c in rule_features_needed if c in out.columns]
    out = out[keep_cols].copy()

    return out

# -------------------------
# Rule evaluation utilities
# -------------------------
def apply_rule(df_syntax: pd.DataFrame, rule_id: str, rule_fn) -> pd.DataFrame:
    """
    Apply a rule evaluator to each row.

    rule_fn must return:
      - 1 (follows), 0 (violates), np.nan (not testable / insufficient data)
    """
    out = df_syntax.copy()
    out["rule_id"] = rule_id
    out["follows_rule"] = out.apply(rule_fn, axis=1)
    out = out.dropna(subset=["follows_rule"]).copy()
    out["follows_rule"] = out["follows_rule"].astype(int)
    out["violates_rule"] = 1 - out["follows_rule"]
    return out

def attach_geo(df_rule_eval: pd.DataFrame, wals_coords: pd.DataFrame) -> pd.DataFrame:
    """Inner join evaluated languages with WALS coordinates + macro metadata."""
    return df_rule_eval.merge(wals_coords, on="lang_code", how="inner")

def macro_area_summary(df_geo: pd.DataFrame) -> pd.DataFrame:
    """Aggregate violation counts/rates by macro-area."""
    return (
        df_geo.groupby("macro_area", dropna=False)
              .agg(
                  n_languages=("lang_code", "nunique"),
                  n_violations=("violates_rule", "sum"),
                  violation_rate=("violates_rule", "mean"),
              )
              .reset_index()
              .sort_values(["n_violations", "n_languages"], ascending=False)
    )
    
def coverage_report(df_syntax: pd.DataFrame, df_eval: pd.DataFrame, df_geo: pd.DataFrame) -> pd.Series:
    """Report coverage: total vs testable vs mappable languages."""
    total_langs = df_syntax["lang_code"].nunique()
    testable_langs = df_eval["lang_code"].nunique()
    mappable_langs = df_geo["lang_code"].nunique()

    return pd.Series({
        "total_languages_in_lang2vec_syntax_df": total_langs,
        "languages_testable_for_rule": testable_langs,
        "testable_fraction": (testable_langs / total_langs) if total_langs else np.nan,
        "languages_with_geo_metadata_after_join": mappable_langs,
        "geo_join_fraction_of_testable": (mappable_langs / testable_langs) if testable_langs else np.nan,
    })
    
def run_rule_from_lang2vec(
    all_syntax_features_df: pd.DataFrame,
    wals_languages_csv_path: str,
    rule_id: str,
    rule_features_needed: List[str],
    rule_fn: Callable
    ):
    """
    Generic pipeline runner for a Greenberg rule using Lang2Vec syntax features.

    Returns a dict with:
      syntax, rule_eval, rule_geo, macro_summary, coverage
    """
    df_syntax = normalize_lang2vec_syntax_df(
        all_syntax_features_df,
        rule_features_needed=rule_features_needed
    )

    # Strict required-column check
    missing = [c for c in rule_features_needed if c not in df_syntax.columns]
    if missing:
        raise ValueError(f"Missing required columns for {rule_id} in Lang2Vec DF: {missing}")

    df_eval = apply_rule(df_syntax, rule_id=f"Greenber_{rule_id}", rule_fn=rule_fn)

    wals_coords = prepare_wals_coords(wals_languages_csv_path)
    df_geo = attach_geo(df_eval, wals_coords)

    macro = macro_area_summary(df_geo)
    coverage = coverage_report(df_syntax, df_eval, df_geo)

    return {
        "syntax": df_syntax,
        "rule_eval": df_eval,
        "rule_geo": df_geo,
        "macro_summary": macro,
        "coverage": coverage,
    }

# -------------------------
# Plotting utilities
# -------------------------
def plot_macro_summary_bar(
    macro_summary: pd.DataFrame,
    rule_id: str,
    macro_col: str = "macro_area",
    y_col: str = "n_violations",
    sort_desc: bool = True,
):
    """
    Plot a bar chart from an already-computed macro_summary table.

    Expected columns (at minimum):
      - macro_col (default: 'macro_area')
      - y_col (default: 'n_violations')

    Common additional columns (used for hover if present):
      - n_languages
      - violation_rate
    """

    if macro_col not in macro_summary.columns:
        raise ValueError(f"macro_col='{macro_col}' not found in macro_summary.columns")

    if y_col not in macro_summary.columns:
        raise ValueError(f"y_col='{y_col}' not found in macro_summary.columns")

    df = macro_summary.copy()

    if sort_desc:
        df = df.sort_values(y_col, ascending=False)

    # Nice hover defaults if those columns exist
    hover = {}
    for col in ["n_languages", "violation_rate"]:
        if col in df.columns:
            hover[col] = True

    fig = px.bar(
        df,
        x=macro_col,
        y=y_col,
        hover_data=hover if hover else None,
        title=f"{rule_id}: {y_col} by macro-area",
    )

    fig.update_layout(
        xaxis_title="Macro-area",
        yaxis_title=y_col.replace("_", " ").title(),
        bargap=0.15,
    )

    fig.show()

def plot_rule_geomap(
    df_geo: pd.DataFrame,
    rule_id: str,
    lat_col: str = "latitude",
    lon_col: str = "longitude",
    violation_col: str = "violates_rule",
    hover_name_col: str = "language_name",
    base_hover_cols: list | None = None,
    extra_hover_cols: list | None = None,
    projection: str = "natural earth",
):
    """
    Plot a reusable geographic scatter map for rule violations.

    Parameters
    ----------
    df_geo : pd.DataFrame
        Rule-evaluated dataframe with geo metadata attached.

    rule_id : str
        Rule identifier for the plot title (e.g., 'Greenberg Rule 20').

    lat_col, lon_col : str
        Column names for latitude and longitude.

    violation_col : str
        Binary column indicating rule violation (1 = violation, 0 = follows).

    hover_name_col : str
        Column used as primary hover label.

    base_hover_cols : list of str, optional
        Core hover columns shared across rules (e.g. lang_code, family, macro_area).

    extra_hover_cols : list of str, optional
        Rule-specific feature columns to include in hover info.

    projection : str
        Map projection type for Plotly.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The generated geographic scatter plot.
    """

    required_cols = {lat_col, lon_col, violation_col}
    missing = required_cols - set(df_geo.columns)
    if missing:
        raise ValueError(f"Missing required columns for geomap: {missing}")

    # Default hover columns
    hover_data = {}

    if base_hover_cols:
        for col in base_hover_cols:
            if col in df_geo.columns:
                hover_data[col] = True

    if extra_hover_cols:
        for col in extra_hover_cols:
            if col in df_geo.columns:
                hover_data[col] = True

    fig = px.scatter_geo(
        df_geo,
        lat=lat_col,
        lon=lon_col,
        color=violation_col,
        hover_name=hover_name_col if hover_name_col in df_geo.columns else None,
        hover_data=hover_data,
        title=f"{rule_id}: testable languages (colored by violation)",
    )

    fig.update_layout(
        geo=dict(
            showland=True,
            showcountries=True,
            projection_type=projection,
        ),
        legend_title_text="Violation",
    )

    fig.show()

