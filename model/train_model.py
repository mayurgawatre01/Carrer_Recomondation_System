# train_model.py
# Trains KNN + Decision Tree on sample student data and saves the model

import pickle
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MinMaxScaler

# ------------------------------------------------------------------
# Sample Training Data
# Features: [python_skill, ml_skill, web_skill, database_skill, aptitude_score, gpa]
# All skills: 0-10, aptitude: 0-100, gpa: 0-10
# ------------------------------------------------------------------
X_train = [
    # python, ml, web, db, aptitude, gpa
    [9, 9, 4, 6, 90, 9.0],   # Data Scientist
    [8, 9, 3, 5, 88, 8.5],   # Data Scientist
    [9, 8, 3, 7, 85, 8.8],   # ML Engineer
    [8, 8, 4, 6, 82, 8.2],   # ML Engineer
    [6, 5, 8, 7, 75, 7.5],   # Data Analyst
    [5, 4, 7, 8, 72, 7.2],   # Data Analyst
    [5, 4, 6, 9, 70, 7.0],   # Cybersecurity Analyst
    [4, 3, 5, 8, 68, 6.8],   # Cybersecurity Analyst
    [6, 4, 9, 6, 74, 7.4],   # Software Developer
    [5, 3, 9, 7, 71, 7.1],   # Software Developer
]

# Labels (career roles)
y_train = [
    'Data Scientist',
    'Data Scientist',
    'ML Engineer',
    'ML Engineer',
    'Data Analyst',
    'Data Analyst',
    'Cybersecurity Analyst',
    'Cybersecurity Analyst',
    'Software Developer',
    'Software Developer',
]

X_train = np.array(X_train)

# Normalize features to [0, 1]
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X_train)

# Train KNN (k=3)
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_scaled, y_train)

# Train Decision Tree
dt = DecisionTreeClassifier(criterion='entropy', max_depth=5, random_state=42)
dt.fit(X_scaled, y_train)

# Save models and scaler
with open('model/career_model.pkl', 'wb') as f:
    pickle.dump({'knn': knn, 'dt': dt, 'scaler': scaler}, f)

print("✅ Models trained and saved successfully!")
