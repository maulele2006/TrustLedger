import pandas as pd

# Load dataset
df = pd.read_csv("data/creditcard.csv")

# Basic information
print("Dataset shape:", df.shape)

print("\nMissing values:")
print(df.isnull().sum().sum())

print("\nTransaction classes:")
print(df["Class"].value_counts())

print("\nFraud percentage:")
print(df["Class"].mean() * 100)