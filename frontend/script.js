// BMI Calculator Script
document.addEventListener('DOMContentLoaded', function() {
    const calculateBtn = document.getElementById('calculate-btn');
    const resetBtn = document.getElementById('reset-btn');
    const bmiCard = document.getElementById('bmi-card');
    const bmiValue = document.getElementById('bmi-value');
    const bmiCategory = document.getElementById('bmi-category');
    const bmiDetails = document.getElementById('bmi-details');
    const unitsSelect = document.getElementById('units');

    // Calculate BMI
    calculateBtn.addEventListener('click', function() {
        const weight = parseFloat(document.getElementById('weight').value);
        const height = parseFloat(document.getElementById('height').value);
        const units = unitsSelect.value;

        if (!weight || !height || weight <= 0 || height <= 0) {
            alert('Please enter valid weight and height values.');
            return;
        }

        let bmi;
        let unitText;

        if (units === 'metric') {
            // Metric: BMI = weight (kg) / (height (m))^2
            const heightM = height / 100; // Convert cm to meters
            bmi = weight / (heightM * heightM);
            unitText = 'kg/m²';
        } else {
            // Imperial: BMI = (weight (lbs) * 703) / (height (inches))^2
            bmi = (weight * 703) / (height * height);
            unitText = 'lbs/in²';
        }

        // Round to 1 decimal place
        const roundedBMI = Math.round(bmi * 10) / 10;

        // Determine category
        let category, details;
        if (roundedBMI < 18.5) {
            category = 'Underweight';
            details = 'Consider consulting a healthcare provider about healthy weight gain strategies.';
        } else if (roundedBMI < 25) {
            category = 'Normal Weight';
            details = 'Great job! Maintain a healthy lifestyle with balanced diet and regular exercise.';
        } else if (roundedBMI < 30) {
            category = 'Overweight';
            details = 'Consider lifestyle changes including diet and exercise to reach a healthier weight.';
        } else {
            category = 'Obese';
            details = 'Please consult a healthcare provider for personalized weight management advice.';
        }

        // Display results
        bmiValue.textContent = `${roundedBMI} ${unitText}`;
        bmiCategory.textContent = category;
        bmiDetails.textContent = details;
        bmiCard.style.display = 'block';

        // Redirect to results page with data
        const username = document.getElementById('username').value;
        const age = document.getElementById('age').value;
        const gender = document.querySelector('input[name="gender"]:checked')?.value || '';
        const activityLevel = document.getElementById('activity').value;

        const params = new URLSearchParams({
            bmi: `${roundedBMI} ${unitText}`,
            category: category,
            details: details,
            username: username,
            age: age,
            gender: gender,
            units: units,
            activity: activityLevel
        });

        // Redirect to results page
        window.location.href = `results.html?${params.toString()}`;
    });

    // Reset form
    resetBtn.addEventListener('click', function() {
        document.getElementById('username').value = '';
        document.getElementById('age').value = '';
        document.getElementById('weight').value = '';
        document.getElementById('height').value = '';
        document.querySelectorAll('input[name="gender"]').forEach(radio => radio.checked = false);
        document.getElementById('activity').value = '3';
        unitsSelect.value = 'metric';
        bmiCard.style.display = 'none';
    });

    // Update placeholders based on units
    unitsSelect.addEventListener('change', function() {
        const weightInput = document.getElementById('weight');
        const heightInput = document.getElementById('height');

        if (this.value === 'metric') {
            weightInput.placeholder = 'eg: 70';
            heightInput.placeholder = 'eg: 175';
        } else {
            weightInput.placeholder = 'eg: 154';
            heightInput.placeholder = 'eg: 69';
        }
    });
});