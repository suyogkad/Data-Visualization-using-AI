# ml/utils.py

import os
import pandas as pd
from app.recommender import recommend_chart

def extract_schema_features(raw_dir: str, output_path: str) -> pd.DataFrame:
    """
    Scan every CSV in `raw_dir`, compute schema features
    (numeric_count, date_count, categorical_count), run the
    existing rule-based recommender to get the chart_type label,
    and save the combined table to `output_path`.
    """
    records = []
    for fname in os.listdir(raw_dir):
        if not fname.lower().endswith('.csv'):
            continue

        path = os.path.join(raw_dir, fname)
        # --- read with fallback encoding ---
        try:
            df = pd.read_csv(path)
        except UnicodeDecodeError:
            df = pd.read_csv(path, encoding='latin1')
        except Exception as e:
            print(f"⚠️ Skipping {fname}: {e}")
            continue

        # Basic dtype counts
        numeric_count     = df.select_dtypes(include='number').shape[1]
        date_count        = df.select_dtypes(include='datetime').shape[1]
        categorical_count = df.select_dtypes(include='object').shape[1]

        # Fallback: parse object columns named “date”
        for col in df.select_dtypes(include='object').columns:
            if 'date' in col.lower():
                try:
                    pd.to_datetime(df[col])
                    date_count += 1
                    categorical_count -= 1
                except:
                    pass

        # Get the rule-based recommendation
        rec = recommend_chart(df)
        chart_type = rec['chart']

        records.append({
            'filename':           fname,
            'numeric_count':      numeric_count,
            'date_count':         date_count,
            'categorical_count':  categorical_count,
            'chart_type':         chart_type
        })

    schema_df = pd.DataFrame(records)
    schema_df.to_csv(output_path, index=False)
    return schema_df
