# Soil Health & Fertilizer Recommendation
# Dataset Enhancement 

import pandas as pd
from core_logic import generate_soil_health, generate_reason, get_cost

# STEP 1: Load Dataset
df = pd.read_csv("dataset/soil_health_fertilizer_recommendation.csv")

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

print("Dataset Loaded")

# STEP 2: Soil Health Column

df["Soil_Health"] = df.apply(
    lambda row: generate_soil_health(
        row["Nitrogen_Level"],
        row["Phosphorus_Level"],
        row["Potassium_Level"],
        row["Soil_pH"]
    ), axis=1)

print("Soil Health Added")

# STEP 3: Cost Column

df["Estimated_Cost"] = df["Recommended_Fertilizer"].apply(get_cost)

print("Cost Added")

# STEP 4: Reason Column

df["Recommendation_Reason"] = df.apply(
    lambda row: generate_reason(
        row["Nitrogen_Level"],
        row["Phosphorus_Level"],
        row["Potassium_Level"],
        row["Crop_Growth_Stage"],
        row["Recommended_Fertilizer"]
    ),
    axis=1
)

print("Reason Added")

# SAVE FINAL DATASET

df.to_csv("dataset/enhanced_dataset.csv", index=False)

print("Dataset Enhancement Completed")

print("\nEnhanced Dataset Saved Successfully!")

# STEP 5: Display Final Dataset Info

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nFinal Dataset Columns:")
print(df.columns)

print("\nFirst 5 Rows:")
print(df.head())

print("\nDataset Enhancement Completed!")