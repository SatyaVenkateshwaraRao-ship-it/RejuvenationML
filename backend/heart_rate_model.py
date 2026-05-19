import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import json

# Load exercise data
df = pd.read_csv('exercise.csv')

# Create a simple age-based heart rate prediction model
# In a real scenario, we'd have more user data
# For now, we'll create a general model based on exercise intensity

# Prepare data for heart rate prediction
X = df[['Duration(minutes)', 'CaloriesBurnt']].values
y = df['Avg Heartrate'].values

# Train Linear Regression model for heart rate prediction
lr_model = LinearRegression()
lr_model.fit(X, y)

# Function to predict heart rate based on exercise parameters
def predict_heart_rate(duration, calories_burnt):
    """Predict heart rate for given exercise parameters"""
    return float(lr_model.predict([[duration, calories_burnt]])[0])

# Function to calculate age-based heart rate zones
def calculate_heart_rate_zones(age):
    """
    Calculate heart rate zones based on age
    Max HR = 220 - age (Karvonen formula)
    """
    max_hr = 220 - age
    
    zones = {
        'max_hr': max_hr,
        'threshold_70_percent': max_hr * 0.70,
        'threshold_80_percent': max_hr * 0.80,
        'threshold_90_percent': max_hr * 0.90,
        'zones': {
            'zone_1_recovery': (max_hr * 0.50, max_hr * 0.60),  # 50-60%
            'zone_2_endurance': (max_hr * 0.60, max_hr * 0.70),  # 60-70%
            'zone_3_tempo': (max_hr * 0.70, max_hr * 0.80),      # 70-80%
            'zone_4_threshold': (max_hr * 0.80, max_hr * 0.90),  # 80-90%
            'zone_5_maximum': (max_hr * 0.90, max_hr * 1.00)     # 90-100%
        }
    }
    
    return zones

# Generate heart rate alerts for all exercises
def generate_hr_alerts(age):
    """Generate alerts for exercises based on age and heart rate"""
    zones = calculate_heart_rate_zones(age)
    threshold = zones['threshold_70_percent']
    
    alerts = []
    
    for idx, row in df.iterrows():
        exercise_hr = row['Avg Heartrate']
        
        alert_level = 'safe'
        message = ''
        
        if exercise_hr >= zones['threshold_90_percent']:
            alert_level = 'critical'
            message = f"🚨 CRITICAL: Heart rate ({exercise_hr} bpm) exceeds 90% of max HR ({zones['max_hr']} bpm)"
        elif exercise_hr >= zones['threshold_80_percent']:
            alert_level = 'warning'
            message = f"⚠️ WARNING: Heart rate ({exercise_hr} bpm) exceeds 80% of max HR ({zones['max_hr']} bpm)"
        elif exercise_hr >= threshold:
            alert_level = 'caution'
            message = f"⏰ CAUTION: Heart rate ({exercise_hr} bpm) exceeds 70% of max HR ({zones['max_hr']} bpm)"
        else:
            alert_level = 'safe'
            message = f"✅ SAFE: Heart rate ({exercise_hr} bpm) is within safe range"
        
        alerts.append({
            'exercise': row['Workout'],
            'phase': row['Phase'],
            'heart_rate': exercise_hr,
            'duration': row['Duration(minutes)'],
            'calories': row['CaloriesBurnt'],
            'alert_level': alert_level,
            'message': message
        })
    
    return alerts, zones

# Test with different ages
test_ages = [25, 30, 40, 50, 60]
output_data = {}

for age in test_ages:
    alerts, zones = generate_hr_alerts(age)
    output_data[age] = {
        'zones': zones,
        'exercise_alerts': alerts,
        'model_coefficients': {
            'duration': float(lr_model.coef_[0]),
            'calories_burnt': float(lr_model.coef_[1]),
            'intercept': float(lr_model.intercept_)
        }
    }

# Save to JSON
with open('heart_rate_model.json', 'w') as f:
    json.dump(output_data, f, indent=2)

print("Heart rate monitoring model generated successfully!")
print(f"Model R² Score: {lr_model.score(X, y):.4f}")
print(f"Model Coefficients: Duration={lr_model.coef_[0]:.4f}, CaloriesBurnt={lr_model.coef_[1]:.4f}")
print(json.dumps(output_data, indent=2))
