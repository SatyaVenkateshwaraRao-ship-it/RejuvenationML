import json

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

# Load exercise data

df = pd.read_csv('exercise.csv')

# Encode categorical variables
le_phase = LabelEncoder()
df['Phase_encoded'] = le_phase.fit_transform(df['Phase'])

le_workout = LabelEncoder()
df['Workout_encoded'] = le_workout.fit_transform(df['Workout'])

# Features and target
X = df[['Duration(minutes)', 'Avg Heartrate', 'Phase_encoded']]
y = df['CaloriesBurnt']

# Train Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=5)
model.fit(X, y)


def find_best_exercises(target_calories, num_suggestions=3):
    """Find best exercises for a given calorie target using the trained model."""

    predictions = []
    for _, row in df.iterrows():
        exercise_data = {
            'workout': row['Workout'],
            'phase': row['Phase'],
            'duration': row['Duration(minutes)'],
            'heartrate': row['Avg Heartrate'],
            'calories_burnt': row['CaloriesBurnt'],
            'efficiency': row['CaloriesBurnt'] / row['Duration(minutes)']
        }
        predictions.append(exercise_data)

    sorted_exercises = sorted(
        predictions,
        key=lambda x: abs(x['calories_burnt'] - target_calories * 0.3)
    )

    top_suggestions = sorted_exercises[:num_suggestions]
    return top_suggestions, sorted_exercises


def get_phase_exercises(phase):
    """Get all exercises from a specific phase."""
    phase_df = df[df['Phase'] == phase]
    exercises = []
    for _, row in phase_df.iterrows():
        exercises.append({
            'workout': row['Workout'],
            'duration': row['Duration(minutes)'],
            'heartrate': row['Avg Heartrate'],
            'calories_burnt': row['CaloriesBurnt'],
            'efficiency': row['CaloriesBurnt'] / row['Duration(minutes)']
        })
    return exercises


def get_all_exercises():
    """Get all exercises organized by phase."""
    return {phase: get_phase_exercises(phase) for phase in df['Phase'].unique()}


def build_recommendations_json():
    """Build the recommendations payload for export or debugging."""
    calorie_levels = [1500, 2000, 2500, 3000]
    recommendations = {}
    for calories in calorie_levels:
        suggestions, _ = find_best_exercises(calories, num_suggestions=5)
        recommendations[calories] = suggestions

    return {
        'recommendations': {str(k): v for k, v in recommendations.items()},
        'all_exercises': get_all_exercises(),
        'feature_importance': {
            'duration': float(model.feature_importances_[0]),
            'heartrate': float(model.feature_importances_[1]),
            'phase': float(model.feature_importances_[2])
        }
    }


if __name__ == '__main__':
    output = build_recommendations_json()
    with open('exercise_data.json', 'w') as f:
        json.dump(output, f, indent=2)

    print('Exercise recommendations generated successfully!')
    print(json.dumps(output, indent=2))
