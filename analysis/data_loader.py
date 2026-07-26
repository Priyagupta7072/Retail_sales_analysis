import pandas as pd
import os


def load_dataset():

    # Paths
    upload_path = "uploads/current_dataset.csv"
    default_path = "data/Superstore.csv"

    # Debug Information
    print("=" * 60)
    print("Upload Exists :", os.path.exists(upload_path))
    print("Upload Path   :", os.path.abspath(upload_path))
    print("Default Path  :", os.path.abspath(default_path))

    # Decide which dataset to load
    if os.path.exists(upload_path):
        file_path = upload_path
        print("Using Uploaded Dataset")
    else:
        file_path = default_path
        print("Using Default Dataset")

    print("Current File :", file_path)

    # Load CSV
    df = pd.read_csv(file_path, encoding="latin1")

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(".", "_", regex=False)
        .str.replace(" ", "_", regex=False)
    )

    print("Columns Found:")
    print(df.columns.tolist())
    print("=" * 60)

    return df