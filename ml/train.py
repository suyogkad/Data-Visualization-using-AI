# ml/train.py

import os
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import classification_report

from ml.utils import extract_schema_features

# --- Configuration ---
RAW_DIR    = 'ml/data/raw'
PROC_DIR   = 'ml/data/processed'
MODEL_DIR  = 'ml/models'

SCHEMA_CSV = os.path.join(PROC_DIR, 'schema_features.csv')
TRAIN_CSV  = os.path.join(PROC_DIR, 'train.csv')
TEST_CSV   = os.path.join(PROC_DIR, 'test.csv')
MODEL_PATH = os.path.join(MODEL_DIR, 'chart_recommender.pkl')

# Allowed chart types for noise injection
CHART_TYPES = ['scatter plot', 'line chart', 'bar chart', 'histogram', 'table']

# --- Synthetic Data Generator with Noise ---
def generate_synthetic_schema(n=1000, noise_rate=0.05):
    """
    Generate n synthetic schema feature rows (numeric_count, date_count,
    categorical_count) with optional label noise at `noise_rate`.
    """
    records = []
    for _ in range(n):
        num = np.random.randint(0, 6)
        date = np.random.randint(0, 4)
        cat = np.random.randint(0, 6)

        # Determine correct label via rule-based logic
        if num >= 2:
            chart = 'scatter plot'
        elif date >= 1 and num >= 1:
            chart = 'line chart'
        elif cat >= 1 and num >= 1:
            chart = 'bar chart'
        elif num >= 1:
            chart = 'histogram'
        else:
            chart = 'table'

        # Inject noise: flip label with probability = noise_rate
        if np.random.rand() < noise_rate:
            alternatives = [c for c in CHART_TYPES if c != chart]
            chart = np.random.choice(alternatives)

        records.append({
            'filename': f'synth_{num}_{date}_{cat}.csv',
            'numeric_count': num,
            'date_count': date,
            'categorical_count': cat,
            'chart_type': chart
        })
    return pd.DataFrame(records)

# --- Main Script ---
def main():
    np.random.seed(42)

    # 1) Ensure directories exist
    os.makedirs(PROC_DIR, exist_ok=True)
    os.makedirs(MODEL_DIR, exist_ok=True)

    # 2) Generate synthetic examples with noise
    print("\n[0/6] Generating 1,000 synthetic schema examples (5% label noise)...")
    df_synth = generate_synthetic_schema(1000, noise_rate=0.05)
    print(f"    ✓ Synthetic examples: {len(df_synth)} rows")

    # 3) Extract real schema features & labels
    print("\n[1/6] Extracting schema features from raw CSVs...")
    df_real = extract_schema_features(RAW_DIR, SCHEMA_CSV)
    print(f"    ✓ Real examples: {len(df_real)} rows saved to {SCHEMA_CSV}")

    # 4) Combine synthetic + real
    df_schema = pd.concat([df_synth, df_real], ignore_index=True)
    print(f"    ✓ Combined dataset size: {len(df_schema)} rows total")

    # 5) Split into train/test
    print("\n[2/6] Splitting into train/test sets (80/20 stratified)...")
    train_df, test_df = train_test_split(
        df_schema,
        test_size=0.2,
        random_state=42,
        stratify=df_schema['chart_type']
    )
    train_df.to_csv(TRAIN_CSV, index=False)
    test_df.to_csv(TEST_CSV, index=False)
    print(f"    ✓ Train: {len(train_df)} rows | Test: {len(test_df)} rows")

    # 6) Train the model with verbose progress
    print("\n[3/6] Training HistGradientBoostingClassifier (verbose)...")
    features = ['numeric_count', 'date_count', 'categorical_count']
    X_train, y_train = train_df[features], train_df['chart_type']

    clf = HistGradientBoostingClassifier(
        verbose=1,       # prints iteration-by-iteration loss
        max_iter=100,
        random_state=42
    )
    clf.fit(X_train, y_train)
    print("    ✓ Training complete")

    # 7) Evaluate on test set
    print("\n[4/6] Evaluating model on test set...")
    X_test, y_test = test_df[features], test_df['chart_type']
    y_pred = clf.predict(X_test)
    report = classification_report(y_test, y_pred)
    print("    ✓ Classification Report:\n")
    print(report)

    # 8) Save the trained model
    print("[5/6] Saving trained model artifact...")
    joblib.dump(clf, MODEL_PATH)
    print(f"    ✓ Model saved to `{MODEL_PATH}`\n")

    # 9) End
    print("[6/6] Training pipeline complete.")

if __name__ == '__main__':
    main()