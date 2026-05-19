import os
from flask import Flask, jsonify, request
from flask_cors import CORS

from exercise_recommendations import (
    build_recommendations_json,
    find_best_exercises,
    get_all_exercises,
    get_phase_exercises,
)
from heart_rate_model import (
    predict_heart_rate,
    calculate_heart_rate_zones,
    generate_hr_alerts,
)

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return jsonify({
        'status': 'ok',
        'message': 'Workout and Calories backend is running',
    })


@app.route('/recommendations', methods=['GET'])
def recommendations():
    try:
        target = float(request.args.get('target', 2000))
        count = int(request.args.get('count', 3))
    except ValueError:
        return jsonify({'error': 'Invalid target or count parameter'}), 400

    suggestions, _ = find_best_exercises(target, num_suggestions=count)
    return jsonify({'target_calories': target, 'suggestions': suggestions})


@app.route('/exercises', methods=['GET'])
def exercises():
    return jsonify({'exercises': get_all_exercises()})


@app.route('/phase/<phase>', methods=['GET'])
def phase_exercises(phase):
    exercises = get_phase_exercises(phase)
    if not exercises:
        return jsonify({'error': f'No exercises found for phase: {phase}'}), 404
    return jsonify({'phase': phase, 'exercises': exercises})


@app.route('/predict-heart-rate', methods=['GET'])
def predict_hr():
    try:
        duration = float(request.args.get('duration', 30))
        calories = float(request.args.get('calories', 200))
    except ValueError:
        return jsonify({'error': 'Invalid duration or calories parameter'}), 400

    predicted = predict_heart_rate(duration, calories)
    return jsonify({'duration': duration, 'calories': calories, 'predicted_heart_rate': predicted})


@app.route('/heart-rate-zones', methods=['GET'])
def heart_rate_zones():
    try:
        age = int(request.args.get('age', 30))
    except ValueError:
        return jsonify({'error': 'Invalid age parameter'}), 400

    zones = calculate_heart_rate_zones(age)
    return jsonify({'age': age, 'zones': zones})


@app.route('/heart-rate-alerts', methods=['GET'])
def heart_rate_alerts():
    try:
        age = int(request.args.get('age', 30))
    except ValueError:
        return jsonify({'error': 'Invalid age parameter'}), 400

    alerts, zones = generate_hr_alerts(age)
    return jsonify({'age': age, 'zones': zones, 'alerts': alerts})


@app.route('/exercise-data', methods=['GET'])
def exercise_data():
    payload = build_recommendations_json()
    return jsonify(payload)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
