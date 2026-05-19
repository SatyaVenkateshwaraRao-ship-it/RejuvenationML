import json

import pandas as pd
from sklearn.linear_model import LinearRegression

# Load exercise data
df = pd.read_csv('exercise.csv')

# Prepare data for heart rate prediction
X = df[['Duration(minutes)', 'CaloriesBurnt']].values
y = df['Avg Heartrate'].values

# Train Linear Regression model for heart rate prediction
lr_model = LinearRegression()
lr_model.fit(X, y)


def predict_heart_rate(duration, calories_burnt):
    """Predict heart rate for given exercise parameters."""
    return float(lr_model.predict([[duration, calories_burnt]])[0])


def calculate_heart_rate_zones(age):
    """Calculate heart rate zones based on age."""
    max_hr = 220 - age
    return {
        'max_hr': max_hr,
        'threshold_70_percent': max_hr * 0.70,
        'threshold_80_percent': max_hr * 0.80,
        'threshold_90_percent': max_hr * 0.90,
        'zones': {
            'zone_1_recovery': (max_hr * 0.50, max_hr * 0.60),
            'zone_2_endurance': (max_hr * 0.60, max_hr * 0.70),
            'zone_3_tempo': (max_hr * 0.70, max_hr * 0.80),
            'zone_4_threshold': (max_hr * 0.80, max_hr * 0.90),
            'zone_5_maximum': (max_hr * 0.90, max_hr * 1.00)
        }
    }


def generate_hr_alerts(age):
    """Generate alerts for exercises based on age and heart rate."""
    zones = calculate_heart_rate_zones(age)
    threshold = zones['threshold_70_percent']
    alerts = []

    for _, row in df.iterrows():
        exercise_hr = row['Avg Heartrate']
        alert_level = 'safe'
        message = f"✅ SAFE: Heart rate ({exercise_hr} bpm) is within safe range"

        if exercise_hr >= zones['threshold_90_percent']:
            alert_level = 'critical'
            message = f"🚨 CRITICAL: Heart rate ({exercise_hr} bpm) exceeds 90% of max HR ({zones['max_hr']} bpm)"
        elif exercise_hr >= zones['threshold_80_percent']:
            alert_level = 'warning'
            message = f"⚠️ WARNING: Heart rate ({exercise_hr} bpm) exceeds 80% of max HR ({zones['max_hr']} bpm)"
        elif exercise_hr >= threshold:
            alert_level = 'caution'
            message = f"⏰ CAUTION: Heart rate ({exercise_hr} bpm) exceeds 70% of max HR ({zones['max_hr']} bpm)"

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


def build_heart_rate_json():
    """Build the heart rate monitoring payload for export or debugging."""
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
    return output_data


if __name__ == '__main__':
    output_data = build_heart_rate_json()
    with open('heart_rate_model.json', 'w') as f:
        json.dump(output_data, f, indent=2)

    print('Heart rate monitoring model generated successfully!')
    print(f'Model R² Score: {lr_model.score(X, y):.4f}')
    print(f'Model Coefficients: Duration={lr_model.coef_[0]:.4f}, CaloriesBurnt={lr_model.coef_[1]:.4f}')
    print(json.dumps(output_data, indent=2))
