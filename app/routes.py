# app/routes.py
from flask import Blueprint, render_template, request, current_app
import pandas as pd

from .recommender import recommend_chart
from .ai import polish_prompt
from .charting import generate_chart_image

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    error = suggestion = notice = chart_uri = None

    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename.lower().endswith(".csv"):
            error = "Please upload a valid .csv file."
        else:
            df = pd.read_csv(file)
            rows, _ = df.shape

            cfg = current_app.config
            # 1) Hard limit
            if rows > cfg["MAX_ROWS_ERROR"]:
                error = (
                    f"Your file has {rows} rows; "
                    f"the maximum allowed is {cfg['MAX_ROWS_ERROR']}."
                )
                return render_template("index.html", error=error)

            # 2) Sampling for mid-sized data
            if rows > cfg["MAX_ROWS_SAMPLE"]:
                df = df.sample(n=cfg["MAX_ROWS_SAMPLE"], random_state=42)
                notice = (
                    f"Dataset had {rows} rows; "
                    f"sampling {cfg['MAX_ROWS_SAMPLE']} rows for recommendation."
                )

            # 3) Recommend chart type
            rec = recommend_chart(df)

            # 4) Avoid huge categorical bars
            if rec["chart"] == "bar chart" and df[rec["x"]].nunique() > cfg["MAX_CAT_UNIQUE"]:
                rec = {"chart": "table"}

            # 5) Build raw suggestion
            if rec["chart"] == "table":
                raw = "This dataset is best explored as a table."
            elif rec["chart"] == "histogram":
                raw = f"Create a histogram of {rec['x']} to see its distribution."
            else:
                raw = f"Create a {rec['chart']} of {rec['x']} versus {rec['y']}."

            # 6) Polish text (optional)
            suggestion = polish_prompt(raw)

            # 7) Generate chart image URI
            chart_uri = generate_chart_image(df, rec)

    return render_template(
        "index.html",
        error=error,
        notice=notice,
        suggestion=suggestion,
        chart_uri=chart_uri
    )
