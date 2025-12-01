import pandas as pd
import numpy as np
import os

# Define the path to the dataset
dataset_path = r'c:\Users\LENOVO\Documents\mL\tunisian_rent_project\data\dataset_loyers_tunisie.csv'

def modify_dataset():
    if not os.path.exists(dataset_path):
        print(f"Error: File not found at {dataset_path}")
        return

    try:
        # Load the dataset
        df = pd.read_csv(dataset_path)
        print("Dataset loaded successfully.")
        print(f"Total rows: {len(df)}")

        # Set random seed for reproducibility
        np.random.seed(42)

        # Add 'Type' column with random mix of 'Location' and 'Vente'
        # Approximately 50% Location and 50% Vente
        if 'Type' not in df.columns:
            df['Type'] = np.random.choice(['Location', 'Vente'], size=len(df), p=[0.5, 0.5])
            print("Added 'Type' column with mixed values.")
        else:
            print("'Type' column already exists. Updating values...")
            df['Type'] = np.random.choice(['Location', 'Vente'], size=len(df), p=[0.5, 0.5])

        # Add 'Prix_vente' column
        # For 'Vente' rows: set Prix_vente based on Loyer (e.g., Loyer * 150 as an estimate)
        # For 'Location' rows: set Prix_vente to 0
        if 'Prix_vente' not in df.columns:
            df['Prix_vente'] = 0
            print("Added 'Prix_vente' column.")
        
        # Update Prix_vente based on Type
        df.loc[df['Type'] == 'Vente', 'Prix_vente'] = (df.loc[df['Type'] == 'Vente', 'Loyer'] * 150).astype(int)
        df.loc[df['Type'] == 'Location', 'Prix_vente'] = 0
        
        print(f"Location count: {(df['Type'] == 'Location').sum()}")
        print(f"Vente count: {(df['Type'] == 'Vente').sum()}")

        # Save the modified dataset
        df.to_csv(dataset_path, index=False)
        print(f"\nDataset saved to {dataset_path}")
        
        # Verify the changes
        print("\nFirst 5 rows of the modified dataset:")
        print(df.head())
        
        print("\nSample of 'Vente' rows:")
        print(df[df['Type'] == 'Vente'].head())

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    modify_dataset()
