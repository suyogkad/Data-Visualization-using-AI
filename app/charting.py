# app/charting.py

import io
import base64
import matplotlib

# Use the Agg backend for PNGs (no GUI)
matplotlib.use('Agg')

import matplotlib.pyplot as plt

def generate_chart_image(df, rec):
    """
    Generate a chart as a base64 PNG data URI, using a non‐interactive Agg backend.
    """
    # Create a fresh Figure+Axes for each call
    fig, ax = plt.subplots()

    chart = rec["chart"]

    if chart == "scatter plot":
        df.plot.scatter(
            x=rec["x"],
            y=rec["y"],
            s=50,
            alpha=0.7,
            ax=ax
        )
        ax.set_xlabel(rec["x"].capitalize())
        ax.set_ylabel(rec["y"].capitalize())

    elif chart == "line chart":
        df.plot.line(
            x=rec["x"],
            y=rec["y"],
            ax=ax
        )
        ax.set_xlabel(rec["x"].capitalize())
        ax.set_ylabel(rec["y"].capitalize())

    elif chart == "bar chart":
        df.plot.bar(
            x=rec["x"],
            y=rec["y"],
            ax=ax
        )
        ax.set_xlabel(rec["x"].capitalize())
        ax.set_ylabel(rec["y"].capitalize())

    elif chart == "histogram":
        df[rec["x"]].plot.hist(
            ax=ax
        )
        ax.set_xlabel(rec["x"].capitalize())
        ax.set_ylabel("Frequency")

    else:
        # Nothing to plot for a “table” recommendation
        plt.close(fig)
        return None

    # Common styling
    title = f"{chart.title()}: {rec['x']}"
    if "y" in rec:
        title += f" vs {rec['y']}"
    ax.set_title(title)
    ax.grid(True)
    fig.tight_layout()

    # Export to base64-encoded PNG
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)   # free memory, avoid GUI calls
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode("ascii")
    return f"data:image/png;base64,{img_b64}"
