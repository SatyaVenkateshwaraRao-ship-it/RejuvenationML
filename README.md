# RejuvenationML

## Overview

RejuvenationML is a health and fitness web application that combines BMI calculation, diet tracking, exercise recommendations, and heart rate monitoring. The project is split into a frontend static site and a Flask-based Python backend, making it easy to deploy the backend on services like Render while keeping the frontend portable.

## Repository Structure

- `backend/`
  - `app.py` — Flask web API entrypoint
  - `exercise_recommendations.py` — recommendation logic and exercise data processing
  - `heart_rate_model.py` — heart rate prediction and zone calculations
  - `exercise.csv` — exercise dataset used by the backend
  - `requirements.txt` — Python dependencies for the backend
  - `Procfile` — Render-compatible startup command
- `frontend/`
  - `index.html` — BMI calculator and user input form
  - `results.html` — BMI results, diet tracking, and navigation
  - `exercises.html` — exercise recommendations and heart rate guidance
  - `script.js` — frontend logic for BMI and diet interactions
  - `style.css` — frontend styles
  - `exercise_data.json` — pre-generated exercise data for static frontend use
- `.gitignore` — ignored files for Python development
- `README.md` — project documentation

## Features

- BMI calculator with metric and imperial units
- Diet tracker with meal selection and calorie summary
- Personalized exercise recommendations based on calories
- Heart rate monitoring guidance by age
- Flask API endpoints for backend calculations
- Ready for deployment to GitHub and Render

## Local Setup

1. Install Python dependencies for the backend:

```bash
cd backend
python -m pip install -r requirements.txt
```

2. Run the backend server:

```bash
cd backend
python app.py
```

3. Serve the frontend locally:

```bash
cd frontend
python -m http.server 8000
```

4. Open the frontend in a browser:

```text
http://127.0.0.1:8000
```

## Backend API Endpoints

- `GET /` — health check
- `GET /recommendations?target=2000&count=3` — get exercise suggestions for a calorie target
- `GET /exercises` — list all exercises grouped by phase
- `GET /phase/<phase>` — list exercises for a specific phase
- `GET /predict-heart-rate?duration=30&calories=200` — predict heart rate
- `GET /heart-rate-zones?age=30` — calculate heart rate zones
- `GET /heart-rate-alerts?age=30` — generate exercise heart rate alerts

## Deployment

### GitHub

Push all changes to the `main` branch with:

```bash
git add .
git commit -m "Update project documentation and deployment setup"
git push origin main
```

### Render

The backend is already configured for Render using `Procfile` and `requirements.txt`.

1. Create a new Web Service on Render.
2. Connect the GitHub repository.
3. Set the root directory to `backend` if needed.
4. Use the build command:

```bash
pip install -r requirements.txt
```

5. Use the start command:

```bash
python app.py
```

## Notes

- The frontend can run as a static site and optionally can be updated to call the backend API directly instead of loading the static JSON file.
- Keep `exercise_data.json` synchronized if the backend data generation changes.
