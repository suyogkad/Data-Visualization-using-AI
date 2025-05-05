# app/recommender.py
import pandas as pd

def recommend_chart(df: pd.DataFrame) -> dict:
    """
    Rule-based chart recommender.
    Returns a dict with keys:
      - chart: one of "scatter plot", "line chart", "bar chart", "histogram", "table"
      - x, y: column names when relevant
    """
    numeric = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    dates   = [c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]

    # Scatter: at least two numeric
    if len(numeric) >= 2:
        return {"chart": "scatter plot", "x": numeric[0], "y": numeric[1]}

    # Line: one date + one numeric
    if dates and numeric:
        return {"chart": "line chart", "x": dates[0], "y": numeric[0]}

    # Bar: one numeric + one categorical
    if numeric:
        cat = next((c for c in df.columns if df[c].dtype == object), None)
        if cat:
            return {"chart": "bar chart", "x": cat, "y": numeric[0]}

    # Histogram: single numeric
    if numeric:
        return {"chart": "histogram", "x": numeric[0]}

    # Fallback: table
    return {"chart": "table"}
