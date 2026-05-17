# predict.py
# Loads saved model and returns ranked career recommendations + skill gaps

import pickle
import numpy as np

# Demand level for each career role
DEMAND = {
    'Data Scientist': 'High',
    'ML Engineer': 'High',
    'Data Analyst': 'Medium',
    'Cybersecurity Analyst': 'Medium',
    'Software Developer': 'High',
}

# Skill gap suggestions per career role
SKILL_GAPS = {
    'Data Scientist': [
        ('Deep Learning', 'https://www.coursera.org/specializations/deep-learning'),
        ('SQL Optimization', 'https://mode.com/sql-tutorial/'),
        ('Cloud (AWS/GCP)', 'https://cloud.google.com/training'),
    ],
    'ML Engineer': [
        ('MLOps', 'https://www.coursera.org/learn/mlops-fundamentals'),
        ('Docker & Kubernetes', 'https://www.docker.com/101-tutorial/'),
        ('Deep Learning', 'https://www.coursera.org/specializations/deep-learning'),
    ],
    'Data Analyst': [
        ('Advanced Excel', 'https://www.coursera.org/learn/excel-data-analysis'),
        ('Tableau / Power BI', 'https://www.tableau.com/learn/training'),
        ('Statistics', 'https://www.khanacademy.org/math/statistics-probability'),
    ],
    'Cybersecurity Analyst': [
        ('Network Security', 'https://www.coursera.org/learn/network-security'),
        ('Ethical Hacking', 'https://www.udemy.com/course/learn-ethical-hacking-from-scratch/'),
        ('Linux Basics', 'https://linuxjourney.com/'),
    ],
    'Software Developer': [
        ('System Design', 'https://www.educative.io/courses/grokking-modern-system-design'),
        ('DSA', 'https://www.geeksforgeeks.org/data-structures/'),
        ('REST APIs', 'https://restfulapi.net/'),
    ],
}


def load_model():
    with open('model/career_model.pkl', 'rb') as f:
        return pickle.load(f)


def get_recommendations(python_skill, ml_skill, web_skill, database_skill, aptitude_score, gpa):
    """
    Returns list of ranked career recommendations with match scores.
    Uses hybrid: KNN probability + Decision Tree probability averaged.
    """
    data = load_model()
    knn = data['knn']
    dt = data['dt']
    scaler = data['scaler']

    # Prepare input
    user_input = np.array([[python_skill, ml_skill, web_skill, database_skill, aptitude_score, gpa]])
    user_scaled = scaler.transform(user_input)

    # Get probabilities from both models
    knn_probs = knn.predict_proba(user_scaled)[0]
    dt_probs = dt.predict_proba(user_scaled)[0]
    classes = knn.classes_

    # Hybrid score: average of KNN and DT probabilities
    hybrid_probs = (knn_probs + dt_probs) / 2

    # Build ranked results
    results = []
    for i, role in enumerate(classes):
        score = round(float(hybrid_probs[i]) * 100, 1)
        results.append({
            'rank': 0,
            'career_role': role,
            'match_score': score,
            'demand': DEMAND.get(role, 'Medium'),
        })

    # Sort by match score descending
    results = sorted(results, key=lambda x: x['match_score'], reverse=True)

    # Assign ranks
    for i, r in enumerate(results):
        r['rank'] = i + 1

    # Skill gaps for top career
    top_role = results[0]['career_role']
    gaps = SKILL_GAPS.get(top_role, [])

    return results, gaps
