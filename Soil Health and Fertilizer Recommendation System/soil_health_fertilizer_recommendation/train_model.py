# Soil Health & Fertilizer Recommendation
# Model Training Module

# Import Libraries
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,  classification_report, confusion_matrix
# Import Preprocessing Function(preprocessing.py)
from preprocessing import preprocess_data

# Load Preprocessed Data

(
    X_train,
    X_test,
    y_train,
    y_test,
    scaler,
    crop_encoder,
    stage_encoder,
    fertilizer_encoder,
    soil_encoder
) = preprocess_data()

print("\nPreprocessed Data Loaded Successfully!")


# Create Random Forest Model

model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)

print("\nRandom Forest Model Created!")


# Train Model
model.fit( X_train, y_train)
print("\nModel Training Completed!")

# Make Predictions

y_pred = model.predict(X_test)

print("\nPrediction Completed!")


# Model Accuracy

accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:")

print(round(accuracy * 100, 2), "%")

# Classification Report

print("\nClassification Report:\n")

print(classification_report(y_test, y_pred))

# Confusion Matrix

print("\nConfusion Matrix:\n")

print(confusion_matrix(y_test, y_pred))


# Save Trained Model

pickle.dump( model, open( "models/fertilizer_model.pkl", "wb"))

print("\nModel Saved Successfully!")

# Save Scaler

pickle.dump( scaler, open("models/scaler.pkl", "wb"))

print("\nScaler Saved Successfully!")

# Save Encoders

pickle.dump(crop_encoder, open( "models/crop_encoder.pkl", "wb" ))

pickle.dump(stage_encoder, open("models/stage_encoder.pkl", "wb"))

pickle.dump(fertilizer_encoder,open("models/fertilizer_encoder.pkl", "wb"))

pickle.dump(soil_encoder, open("models/soil_encoder.pkl", "wb"))

print("\nEncoders Saved Successfully!")


# Feature Importance

feature_names = [
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

importance = model.feature_importances_

print("\nFeature Importance:\n")

for feature, score in zip(feature_names, importance):
    print(feature, ":", round(score, 4))

print("\nModel Training Pipeline Completed Successfully!")