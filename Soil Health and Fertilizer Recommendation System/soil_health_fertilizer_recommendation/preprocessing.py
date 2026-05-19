# Soil Health & Fertilizer Recommendation
# Data Preprocessing Module

# Import Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Preprocessing Function

def preprocess_data():

    # Load Dataset

    df = pd.read_csv("dataset/enhanced_dataset.csv")

    print("\nDataset Loaded Successfully!")

    # Basic Dataset Information

    print("\nDataset Information:\n")

    df.info()

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumn Names:")
    print(df.columns)

    # Check Missing Values

    print("\nMissing Values:\n")

    print(df.isnull().sum())

    # Remove Missing Values

    df = df.dropna()

    print("\nMissing Values Removed!")

    # Remove Duplicate Rows

    duplicate_count = df.duplicated().sum()

    print("\nDuplicate Rows Found:")
    print(duplicate_count)

    df = df.drop_duplicates()

    print("\nDuplicate Rows Removed!")

    # Check Data Types

    print("\nData Types Before Conversion:\n")

    print(df.dtypes)

    # Convert Numerical Columns

    numerical_columns = [
        "Soil_pH",
        "Nitrogen_Level",
        "Phosphorus_Level",
        "Potassium_Level",
        "Temperature",
        "Humidity",
        "Rainfall",
        "Estimated_Cost"
    ]

    for column in numerical_columns:

        df[column] = pd.to_numeric(df[column])

    print("\nNumerical Columns Converted!")

    # Convert Categorical Columns

    categorical_columns = [
        "Crop_Type",
        "Crop_Growth_Stage",
        "Recommended_Fertilizer",
        "Soil_Health",
        "Recommendation_Reason"
    ]

    for column in categorical_columns:
        df[column] = df[column].astype(str)

    print("\nCategorical Columns Converted!")

    # Check Data Types Again

    print("\nData Types After Conversion:\n")

    print(df.dtypes)

    # Remove Rows Created by Conversion Errors

    df = df.dropna()
    print("\nInvalid Rows Removed!")


    # Encode Categorical Columns

    crop_encoder = LabelEncoder()

    # df["Crop_Type"] = (crop_encoder.fit_transform(df["Crop_Type"]))
    df["Crop_Type"] = crop_encoder.fit_transform(df["Crop_Type"])

    stage_encoder = LabelEncoder()

    df["Crop_Growth_Stage"] = (stage_encoder.fit_transform(df["Crop_Growth_Stage"]))

    fertilizer_encoder = LabelEncoder()

    df["Recommended_Fertilizer"] = (fertilizer_encoder.fit_transform(df["Recommended_Fertilizer"]))

    soil_encoder = LabelEncoder()

    df["Soil_Health"] = (soil_encoder.fit_transform(df["Soil_Health"]))

    print("\nCategorical Columns Encoded!")

    # Feature Selection

    X = df[
        [
            "Soil_pH",
            "Nitrogen_Level",
            "Phosphorus_Level",
            "Potassium_Level",
            "Temperature",
            "Humidity",
            "Rainfall",
            "Crop_Type",
            "Crop_Growth_Stage"
        ]
    ]

    # Target Variable

    y = df["Recommended_Fertilizer"]

    # Feature Scaling
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("\nFeature Scaling Applied!")

    # Train-Test Split

    (X_train, X_test, y_train, y_test) = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    print("\nTrain-Test Split Completed!")

    # Final Dataset Information

    print("\nTraining Shape:")
    print(X_train.shape)

    print("\nTesting Shape:")
    print(X_test.shape)

    print("\nFinal Dataset Shape:")
    print(df.shape)

    print("\nPreprocessing Completed Successfully!")

    # Return Processed Data

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler,
        crop_encoder,
        stage_encoder,
        fertilizer_encoder,
        soil_encoder
    )